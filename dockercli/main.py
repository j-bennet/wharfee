#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import os
import click

from prompt_toolkit import AbortAction, Exit
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.contrib.shortcuts import create_cli
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.history import FileHistory
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from .client import DockerClient
from .client import DockerClientException


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

        self.keyword_completer = WordCompleter(
            ['help',
             'version',
             'ps',
             'images',
             'run',
             'stop'],
            ignore_case=False)

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

    def run_cli(self):
        """
        Run the main loop
        :return:
        """

        cli = create_cli(
            'dockercli> ',
            style=DocumentStyle,
            completer=self.keyword_completer,
            history_filename=os.path.expanduser('~/.dockercli-history'))

        while True:
            try:
                document = cli.read_input(
                    on_exit=AbortAction.RAISE_EXCEPTION)

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