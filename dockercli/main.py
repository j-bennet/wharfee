#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

from prompt_toolkit.contrib.shortcuts import get_input
from prompt_toolkit.history import History
from prompt_toolkit.contrib.completers import WordCompleter


class DockerCli(object):

    def __init__(self):
        self.keyword_completer = WordCompleter(
            ['ps',
             'images',
             'run',
             'stop'],
            ignore_case=False)

    def run_cli(self):
        """
        Run the main loop
        :return:
        """
        history = History()

        while True:
            text = get_input("> ", completer=self.keyword_completer)
            if text is None:
                break
            print('You entered:', text)

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