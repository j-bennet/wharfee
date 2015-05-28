#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import os
import click

from types import GeneratorType
from prompt_toolkit import AbortAction
from prompt_toolkit import CommandLineInterface
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.contrib.shortcuts import create_default_layout
from prompt_toolkit.contrib.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.history import FileHistory
from prompt_toolkit.keys import Keys
from pygments.token import Token

from .client import DockerClient
from .client import DockerPermissionException
from .client import DockerTimeoutException
from .client import DockerSslException
from .completer import DockerCompleter
from .lexer import CommandLexer
from .formatter import format_data
from .formatter import COMMAND_FORMATTERS
from .config import write_default_config
from .config import read_config
from .style import style_factory


class DockerCli(object):
    """
    The CLI implementation.
    """

    keyword_completer = None
    handler = None
    saved_less_opts = None
    config = None
    config_template = 'dockerclirc'
    config_name = '~/.dockerclirc'

    def __init__(self):
        """
        Initialize class members.
        Should read the config here at some point.
        """

        self.config = self.read_configuration()
        self.theme = self.config['main']['theme']
        self.handler = DockerClient(
            self.config['main'].as_int('client_timeout'))
        self.completer = DockerCompleter()
        self.set_completer_options()
        self.saved_less_opts = self.set_less_opts()

    def read_configuration(self):
        """

        :return:
        """
        default_config = os.path.join(
            self.get_package_path(), self.config_template)
        write_default_config(default_config, self.config_name)
        return read_config(self.config_name, default_config)

    def get_package_path(self):
        """
        Find out pakage root path.
        :return: string: path
        """
        from dockercli import __file__ as package_root
        return os.path.dirname(package_root)

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

    def set_completer_options(self, cons=True, runs=True, imgs=True):
        """
        Set image and container names in Completer.
        Re-read if needed after a command.
        :param cons: boolean: need to refresh containers
        :param runs: boolean: need to refresh running containers
        :param imgs: boolean: need to refresh images
        """

        if cons:
            cs = self.handler.containers(all=True)
            if cs and len(cs) > 0 and isinstance(cs[0], dict):
                containers = [name for c in cs for name in c['Names']]
                self.completer.set_containers(containers)

        if runs:
            cs = self.handler.containers()
            if cs and len(cs) > 0 and isinstance(cs[0], dict):
                running = [name for c in cs for name in c['Names']]
                self.completer.set_running(running)

        if imgs:
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
            style=style_factory(self.theme),
            on_exit=AbortAction.RAISE_EXCEPTION)

        while True:
            try:
                document = dcli.read_input()
                self.handler.handle_input(document.text)
                formatter = COMMAND_FORMATTERS.get(self.handler.command, None)

                if isinstance(self.handler.output, GeneratorType):
                    for line in self.handler.output:
                        if formatter:
                            line = formatter(line)
                        else:
                            line = line.strip()
                        click.echo(line)
                else:
                    lines = format_data(self.handler.output)
                    click.echo_via_pager('\n'.join(lines))

                if self.handler.after:
                    for line in self.handler.after():
                        click.echo(line)

                # After processing the command, refresh the lists of
                # containers and images as needed
                self.set_completer_options(self.handler.is_refresh_containers,
                                           self.handler.is_refresh_running,
                                           self.handler.is_refresh_images)

            except KeyboardInterrupt:
                # user pressed Ctrl + C
                if self.handler.after:
                    click.echo('')
                    for line in self.handler.after():
                        click.echo(line)

            except DockerPermissionException as ex:
                click.secho(ex.message, fg='red')

            except EOFError:
                # exit out of the CLI
                break

            #except Exception as ex:
            #    click.secho("{0}".format(ex), fg='red')
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
    except DockerTimeoutException as ex:
        click.secho(ex.message, fg='red')
    except DockerSslException as ex:
        click.secho(ex.message, fg='red')

if __name__ == "__main__":
    cli()