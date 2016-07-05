# -*- coding: utf-8
"""
Docker option checker / helper.

Usage:
    optionizer.py
    optionizer.py <command>
    optionizer.py [--implemented|--unimplemented]

-h --help           Show this help
-i --implemented    Show implemented commands only
-u --unimplemented  Show unimplemented commands only
<command>           Specify command to review
"""
from __future__ import unicode_literals
from __future__ import print_function

import re
import click
import pexpect
import wharfee.options as opts

from docopt import docopt
from tabulate import tabulate


usage = __doc__


def get_all_commands():
    """Retrieve all docker commands.
    :return: set of strings
    """
    txt = pexpect.run('docker').strip().splitlines(False)
    all_commands = set()
    in_commands = False

    for line in txt:
        if in_commands:
            if line:
                all_commands.add(line.strip().split(' ', 1)[0])
            else:
                break
        if line.lower() == 'commands:':
            in_commands = True

    return all_commands


def get_command_details(command):
    """
    Parse arguments, options and subcommands out of command docstring.
    :param command: string main command
    :return: tuple of (commands, options, arguments)
    """
    txt = pexpect.run('docker {} --help'.format(command)).strip().splitlines(False)
    in_commands = False
    in_options = False

    commands = set()
    options = set()
    arguments = {}

    arg_parts = re.split('\s+', txt[0])[3:]
    for arg in arg_parts:
        arg_name = arg.lstrip('[').rstrip('.]')
        if arg_name in arguments:
            arguments[arg_name]['mul'] = True
        else:
            arguments[arg_name] = {
                'mul': '...' in arg,
                'opt': arg.startswith('[')
            }

    for line in txt:
        line = line.strip()

        if not line:
            in_commands, in_options = False, False
        elif in_commands:
            cmd, _ = re.split('\s{2,}', line, 1)
            commands.add(cmd)
        elif in_options:
            opt, desc = re.split('\s{2,}', line, 1)
            options.add((opt, desc))

        if line.lower() == 'commands:':
            in_commands = True

        if line.lower() == 'options:':
            in_options = True

    return commands, options, arguments


def check_commands(args):
    """
    Display information about implemented and unimplemented commands.
    """
    is_impl = args['--implemented']
    is_unimpl = args['--unimplemented']
    all_commands = get_all_commands()
    implemented = set([c.split(' ', 1)[0] for c in opts.COMMAND_NAMES])

    if is_impl:
        result = implemented
    elif is_unimpl:
        result = all_commands - implemented
    else:
        result = all_commands

    info = [(c, 'Y' if c in implemented else 'N')
                for c in sorted(result)]
    click.echo_via_pager(tabulate(info, headers=('Command', 'Implemented')))


def check_command(command):
    """
    Display information about implemented and unimplemented options.
    """
    commands, options, arguments = get_command_details(command)
    from pprint import pprint
    pprint(commands)
    pprint(options)
    pprint(arguments)


def main():
    """
    Display information on implemented commands and options.
    :param command: string command name
    """
    global usage
    args = docopt(usage)
    command = args['<command>']
    if command:
        check_command(command)
    else:
        check_commands(args)


if __name__ == '__main__':
    main()
