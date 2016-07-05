# -*- coding: utf-8
"""
Docker option checker / helper.

Usage:
    optionizer.py [<command>] [--implemented|--unimplemented]

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
import textwrap
import wharfee.options as opts

from docopt import docopt
from tabulate import tabulate
from jinja2 import Template
from collections import namedtuple


usage = __doc__


OptInfo = namedtuple(
    'OptInto',
    [
        'type_str',
        'short_name',
        'long_name',
        'action',
        'dest',
        'help',
        'default',
        'nargs',
    ]
)


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


def get_option_info(name, desc):
    """
    Create an instance of OptInfo out of option name and description.
    :param name: str
    :param desc: str
    :return: OptInfo
    """
    short_name = long_name = arg = None
    for token in name.split():
        if token.startswith('--'):
            long_name = token.strip(',')
        elif token.startswith('-'):
            short_name = token.strip(',')
        else:
            arg = token

    action = 'store' if arg else 'store_true'
    const_type = 'TYPE_STRING' if arg else 'TYPE_BOOLEAN'
    dest = clean_name(long_name)
    default = default_value(desc)
    return OptInfo(
        type_str=const_type,
        short_name=short_name,
        long_name=long_name,
        action=action,
        dest=dest,
        default=default,
        help=desc,
        nargs=None
    )


def get_command_details(command):
    """
    Parse arguments, options and subcommands out of command docstring.
    :param command: string main command
    :return: tuple of (help, commands, options, arguments)
    """
    txt = pexpect.run('docker {} --help'.format(command)).strip().splitlines(False)
    in_commands = False
    in_options = False

    commands = set()
    options = set()
    arguments = {}
    help = txt[2]

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

    return help, commands, options, arguments


def get_implemented_commands():
    """Get all implemented command names.
    :return: set of strings
    """
    return set([c.split(' ', 1)[0] for c in opts.COMMAND_NAMES])


def check_commands(args):
    """
    Display information about implemented and unimplemented commands.
    """
    is_impl = args['--implemented']
    is_unimpl = args['--unimplemented']
    all_commands = get_all_commands()
    implemented = get_implemented_commands()

    if is_impl:
        result = implemented
    elif is_unimpl:
        result = all_commands - implemented
    else:
        result = all_commands

    info = [(c, 'Y' if c in implemented else 'N')
                for c in sorted(result)]
    click.echo_via_pager(tabulate(info, headers=('Command', 'Implemented')))


def format_subcommands(commands):
    """Format subcommands for display.
    :param commands: list of strings
    :return: string
    """
    return '\n'.join(commands)


def default_value(desc):
    """
    Parse default out of description.
    :param desc: str
    :return: str
    """
    subs = {
        'true': True,
        'false': False
    }
    if '(default' in desc:
        _, result = desc.split('(default ')
        result = result.rstrip(')')
        result = subs.get(result, result)
        return result
    return None


def clean_name(command_name):
    """
    Turn long option name into valid python identifier: "--all" -> "all".
    :param command_name: str
    :return: string
    """
    if '-' not in command_name:
        return command_name
    result = command_name.lstrip('-')
    result = re.sub('\-', '_', result)
    return result


def format_option(info):
    """
    Format code to create CommandOption.
    :param info: OptInfo
    :return: string
    """
    quote = lambda x: "'{}'".format(x) if x is not None else x
    tmpl = Template("""
    CommandOption(
        CommandOption.{{ const_type }},
        {{ short_name }},
        {{ long_name }},
        action='{{ action }}',
        dest='{{ dest }}',{% if default is not none %}
        default={{ default }},{% endif %}
        help='{{ help }}.'
    ),
    """)
    result = tmpl.render(
        const_type=info.type_str,
        short_name=quote(info.short_name),
        long_name=quote(info.long_name),
        action=info.action,
        dest=info.dest,
        default=info.default,
        help=info.help.rstrip('.')
    )
    return textwrap.dedent(result).strip()


def format_options(options):
    """
    Format options for display.
    :param options: list of (name, description)
    :return: string
    """
    return '\n'.join([format_option(get_option_info(name, desc))
                      for name, desc in options])


def format_arguments(arguments):
    """
    Format arguments for display.
    :param arguments: dict
    :return: string
    """
    from pprint import pformat
    return pformat(arguments)


def check_command(command, args):
    """
    Display information about implemented and unimplemented options.
    :param command: str
    :param args: dict
    """
    implemented = get_implemented_commands()
    is_impl = args['--implemented']
    is_unimpl = args['--unimplemented']
    help, commands, options, arguments = get_command_details(command)
    print(textwrap.dedent('''
    Command: [docker] {command}
    Help: {help}
    Subcommands: {subs}
    Implemented: {implemented}'''.format(
        command=command,
        implemented='Yes' if command in implemented else 'No',
        subs=len(commands) if commands else 'No',
        help=help)))

    if commands:
        print('Subcommands:')
        print(format_subcommands(commands))
        print()

    print(textwrap.dedent('''
    Options:
    --------'''))
    print(format_options(options))

    print(textwrap.dedent('''
    Arguments:
    ----------'''))
    print(format_arguments(arguments))


def main():
    """
    Display information on implemented commands and options.
    :param command: string command name
    """
    global usage
    args = docopt(usage)
    command = args['<command>']
    if command:
        check_command(command, args)
    else:
        check_commands(args)


if __name__ == '__main__':
    main()
