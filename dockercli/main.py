#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import os
import click

from prompt_toolkit import AbortAction
from prompt_toolkit import CommandLineInterface
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.contrib.shortcuts import create_default_layout
from prompt_toolkit.contrib.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.history import FileHistory
from prompt_toolkit.keys import Keys
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from .client import DockerClient
from .client import DockerPermissionException
from .client import DockerSslException
from .completer import DockerCompleter
from .lexer import CommandLexer
from .formatter import format_data

class DocumentStyle(Style):
    """
    Encapsulates visual styles for the CLI.
    TODO: move to a config file.
    """
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


class DockerCli(object):
    """
    The CLI implementation.
    """

    keyword_completer = None
    handler = None
    saved_less_opts = None

    def __init__(self):
        """
        Initialize class members.
        Should read the config here at some point.
        """

        self.handler = DockerClient()
        self.completer = DockerCompleter()
        self.set_completer_options()
        self.saved_less_opts = self.set_less_opts()

    def set_less_opts(self):
        """
        Set the "less" options and save the old settings.

        What we're setting:
          -F:
            --quit-if-one-screen: Quit if entire file fits on first screen.
          -R:
            --raw-control-chars: Output "raw" control characters.
          -X:
            --no-init: Don't use termcap keypad init/deinit strings.
            --no-keypad: Don't use termcap init/deinit strings.
            This also disables launching "less" in an alternate screen.

        :return: string with old options
        """
        opts = os.environ.get('LESS', '')
        os.environ['LESS'] = '-RXF'
        return opts

    def revert_less_opts(self):
        """
        Restore the previous "less" options.
        """
        os.environ['LESS'] = self.saved_less_opts

    def get_toolbar_items(self, cli):
        """
        Return bottom menu items
        :param cli:
        :return: list of Token.Toolbar
        """
        return [
            (Token.Toolbar.Status, ' [F2] Help '),
            (Token.Toolbar.Status, ' [F10] Exit ')
        ]

    def get_key_manager(self):
        """
        Create and initialize keybinding manager
        :return: KeyBindingManager
        """
        manager = KeyBindingManager()

        @manager.registry.add_binding(Keys.F2)
        def _(event):
            """
            When F2 has been pressed, fill in the "help" command.
            """
            event.cli.current_buffer.insert_text("help")

        @manager.registry.add_binding(Keys.F10)
        def _(event):
            """
            When F10 has been pressed, quit.
            """
            # Unused parameters for linter.
            _ = event
            raise EOFError

        return manager

    def set_completer_options(self):
        """
        Set image and container names in Completer.
        Re-read them every time we run a command, because
        things might have changed.
        """
        containers = []
        running = []
        images = []

        cs = self.handler.containers(all=True)
        if cs and len(cs) > 0 and isinstance(cs[0], dict):
            containers = [name for c in cs for name in c['Names']]
            self.completer.set_containers(containers)

        cs = self.handler.containers()
        if cs and len(cs) > 0 and isinstance(cs[0], dict):
            running = [name for c in cs for name in c['Names']]
            self.completer.set_running(running)

        def parse_image_name(tag):
            if ':' in tag:
                return tag.split(':', 2)[0]
            return tag

        ims = self.handler.images()
        if ims and len(ims) > 0 and isinstance(ims[0], dict):
            images = set([])
            tagged = set([])
            for im in ims:
                for name in im['RepoTags']:
                    images.add(parse_image_name(name))
                    tagged.add(name)
            self.completer.set_images(images)
            self.completer.set_tagged(tagged)

    def run_cli(self):
        """
        Run the main loop
        """

        history = FileHistory(os.path.expanduser('~/.dockercli-history'))

        layout = create_default_layout(
            message='dockercli> ',
            reserve_space_for_menu=True,
            lexer=CommandLexer,
            get_bottom_toolbar_tokens=self.get_toolbar_items)

        buffer = Buffer(
            history=history,
            completer=self.completer,
        )

        manager = self.get_key_manager()
        eventloop = create_eventloop()

        dcli = CommandLineInterface(
            eventloop,
            layout=layout,
            buffer=buffer,
            key_bindings_registry=manager.registry,
            style=DocumentStyle,
            on_exit=AbortAction.RAISE_EXCEPTION)

        while True:
            try:
                document = dcli.read_input()
                self.set_completer_options()
                self.handler.handle_input(document.text)
                if self.handler.is_stream:
                    for line in self.handler.output:
                        if self.handler.stream_formatter:
                            line = self.handler.stream_formatter(line)
                        else:
                            line = line.strip()
                        click.echo(line)
                else:
                    lines = format_data(self.handler.output)
                    click.echo_via_pager('\n'.join(lines))

            except DockerPermissionException as ex:
                click.secho(ex.message, fg='red')

            except EOFError:
                # exit out of the CLI
                break

            #except Exception as ex:
            #    click.secho(ex.message, fg='red')
            #    break

        self.revert_less_opts()
        print('Goodbye!')


@click.command()
def cli():
    """
    Create and call the CLI
    """
    try:
        dockercli = DockerCli()
        dockercli.run_cli()
    except DockerSslException as ex:
        click.secho(ex.message, fg='red')

if __name__ == "__main__":
    cli()