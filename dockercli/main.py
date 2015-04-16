#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import click

from prompt_toolkit.contrib.shortcuts import get_input
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from .client import DockerClient
from .client import DockerClientException


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)

class DockerCli(object):

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

    def run_cli(self):
        """
        Run the main loop
        :return:
        """

        while True:
            try:
                text = get_input(
                    "dockercli> ",
                    completer=self.keyword_completer,
                    style=DocumentStyle,
                    history_filename='.dockercli_history'
                )

                # Ctrl + C was pressed
                if text is None:
                    break

                output = self.handler.handle_input(text)
                click.echo_via_pager('\n'.join(output))

            except DockerClientException as ex:
                click.echo(ex.message, color='red')

            except EOFError:
                break

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