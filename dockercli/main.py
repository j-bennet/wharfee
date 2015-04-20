#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import os
import click

from prompt_toolkit import AbortAction
from prompt_toolkit import Exit
from prompt_toolkit import CommandLineInterface
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.contrib.shortcuts import create_default_layout
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.history import FileHistory
from prompt_toolkit.keys import Keys
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from .client import DockerClient
from .client import DockerClientException
from .completer import DockerCompleter


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

        self.completer = DockerCompleter()
        self.handler = DockerClient()
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
            raise Exit()

        return manager

    def run_cli(self):
        """
        Run the main loop
        """

        history = FileHistory(os.path.expanduser('~/.dockercli-history'))

        layout = create_default_layout(
            message='dockercli> ',
            reserve_space_for_menu=True,
            get_bottom_toolbar_tokens=self.get_toolbar_items)

        buffer = Buffer(
            history=history,
            completer=self.completer,
        )

        manager = self.get_key_manager()

        cli = CommandLineInterface(
            layout=layout,
            buffer=buffer,
            key_bindings_registry=manager.registry,
            style=DocumentStyle)

        while True:
            try:
                document = cli.read_input(
                    on_exit=AbortAction.RAISE_EXCEPTION
                )

                output = self.handler.handle_input(document.text)
                click.echo_via_pager('\n'.join(output))

            except DockerClientException as ex:
                click.secho(ex.message, fg='red')

            except Exit:
                # exit out of the CLI
                break

            except Exception as ex:
                click.secho(ex.message, fg='red')
                break

        self.revert_less_opts()
        print('Goodbye!')

def cli():
    """
    Create and call the CLI
    :return:
    """
    dockercli = DockerCli()
    dockercli.run_cli()

if __name__ == "__main__":
    cli()