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

import os
import re
import pexpect
import textwrap
import six
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


def is_in_files(dir_name, file_ext, search_str):
    """
    If any of the given strings present in files.
    :param dir_name: str
    :param file_ext: str
    :param search_str: list
    :return: boolean
    """
    for file_name in os.listdir(dir_name):
        if file_name.endswith(file_ext):
            with open(os.path.join(dir_name, file_name), 'r') as f:
                for line in f:
                    if any([s in line for s in search_str]):
                        return True
    return False


def is_in_steps(command):
    """See if command is mentioned in step files.
    :return: boolean
    """
    current_dir = os.path.dirname(__file__)
    step_dir = os.path.abspath(os.path.join(current_dir, '../tests/features/steps/'))
    feature_dir = os.path.abspath(os.path.join(current_dir, '../tests/features/'))
    return is_in_files(step_dir, '.py', ['sendline("{0}'.format(command), "sendline('{0}".format(command)]) or \
           is_in_files(feature_dir, '.feature', ['docker {0}'.format(command)])


def get_all_commands():
    """Retrieve all docker commands.
    :return: set of str
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

    default = default_value(desc)
    nargs = None

    if not arg:
        action = 'store_true'
    elif default == '[]':
        action = 'append'
        nargs = '*'
    else:
        action = 'store'

    const_type = 'TYPE_STRING' if arg else 'TYPE_BOOLEAN'
    dest = clean_name(long_name)
    return OptInfo(
        type_str=const_type,
        short_name=short_name,
        long_name=long_name,
        action=action,
        dest=dest,
        default=default,
        help=desc,
        nargs=nargs
    )


def tokenize_usage(command, usage_str):
    """
    Split usage string into groups of arguments.
    :param command: str
    :param usage_str: str
    :return: list
    """
    i_command_end = usage_str.find(command)
    arg_str = usage_str[i_command_end + len(command) + 1:]
    tokens = arg_str.split()
    for i, token in enumerate(tokens):
        if token == '|':
            # next token is an OR of previous one. Skip it.
            if i < len(tokens) - 1:
                tokens[i + 1] = '|'
    return [t for t in tokens if t != '|']


def get_command_arguments(command, usage_str):
    """
    Get command arguments out of usage string.
    :param command: str
    :param usage_str: str
    :return: list
    """
    # Usage:	docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
    ars = tokenize_usage(command, usage_str)
    arg_dict = {}
    result = []
    for arg in ars:
        if arg == '[OPTIONS]':
            continue
        long_name = clean_name(arg).lower()
        is_optional = '[' in arg
        is_multiple = '.' in arg
        if long_name in arg_dict:
            arg_dict[long_name]['mul'] = True
        else:
            arg_dict[long_name] = {
                'mul': is_multiple,
                'opt': is_optional
            }
    for long_name, props in arg_dict.items():
        action = 'append' if props['mul'] else 'store'
        if props['mul'] and props['opt']:
            nargs = '*'
        elif props['mul']:
            nargs = '+'
        else:
            nargs = None
        result.append(OptInfo(
            type_str='TYPE_STRING',
            short_name=None,
            long_name=long_name,
            action=action,
            dest=long_name,
            default=None,
            help='<Add help here>',
            nargs=nargs
        ))
    return result


def get_command_details(command):
    """
    Parse arguments, options and subcommands out of command docstring.
    :param command: str main command
    :return: tuple of (usage, help, commands, options, arguments)
    """
    txt = pexpect.run('docker {} --help'.format(command)).strip().splitlines(False)
    in_commands = False
    in_options = False

    commands = set()
    options = set()
    usage_str = txt[0]
    descr = txt[2]
    arguments = get_command_arguments(command, txt[0])

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

    return usage_str, descr, commands, options, arguments


def get_implemented_commands():
    """Get all implemented command names.
    :return: set of str
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

    info = [(c, 'Y' if c in implemented else 'N', 'Y' if is_in_steps(c) else 'N')
            for c in sorted(result)]
    print(tabulate(info, headers=('Command', 'Implemented', 'Tested')))


def format_subcommands(commands):
    """Format subcommands for display.
    :param commands: list of str
    :return: str
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


def clean_name(opt_name):
    """
    Turn long option name into valid python identifier: "--all" -> "all".
    :param opt_name: str
    :return: str
    """
    if not re.match('[^A-Za-z_]', opt_name):
        return opt_name
    result = opt_name.strip('[]')
    result = result.rstrip('.')
    result = result.lstrip('-')
    result = re.sub('[^A-Za-z_]', '_', result)
    return result


def maybe_quote(x):
    """
    Quote if it looks like string
    :param x: object
    :return: object
    """
    if not isinstance(x, six.string_types):
        return x
    if x.lower() in ['true', 'false', 'none']:
        return x
    if re.match('^[0-9]+\.?[0-9]*$', x):
        return x
    return "'{}'".format(x)


def format_option(info):
    """
    Format code to create CommandOption.
    :param info: OptInfo
    :return: str
    """
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
        short_name=maybe_quote(info.short_name),
        long_name=maybe_quote(info.long_name),
        action=info.action,
        dest=info.dest,
        default=maybe_quote(info.default),
        help=info.help.rstrip('.')
    )
    return textwrap.dedent(result).strip()


def get_implemented_arguments(command):
    """
    Get all implemented argument names for the command.
    :param command: str
    :return: set of str
    """
    if command not in opts.COMMAND_NAMES:
        return []

    result = set(o.name
                 for o in opts.COMMAND_OPTIONS.get(command, [])
                 if not o.name.startswith('-'))
    return result


def get_implemented_options(command):
    """
    Get all implemented option names for the command.
    :param command: str
    :return: set of tuples (short_name, long_name)
    """
    if command not in opts.COMMAND_NAMES:
        return []

    result = set([(o.short_name, o.long_name)
                  for o in opts.COMMAND_OPTIONS.get(command, [])
                  if o.name.startswith('-')])
    result.add((None, '--help'))
    result.add(('-h', '--help'))
    return result


def format_options(command, options, is_impl, is_unimpl, header=True):
    """
    Format options for display.
    :param command: str
    :param options: list of (name, description)
    :param is_impl: boolean only show implemented
    :param is_unimpl: boolean only show unimplemented
    :param header: boolean add header
    :return: str
    """
    implemented_opts = get_implemented_options(command)
    infos = [get_option_info(name, desc) for name, desc in options]
    if is_impl:
        infos = [i for i in infos if (i.short_name, i.long_name) in implemented_opts]
    elif is_unimpl:
        infos = [i for i in infos if (i.short_name, i.long_name) not in implemented_opts]
    result = '\n'.join([format_option(info)
                        for info in infos])
    if header:
        result = format_header('Options', len(infos), len(options), is_impl, is_unimpl) \
                 + '\n' \
                 + result
    return result


def format_arguments(command, arguments, is_impl, is_unimpl, header=True):
    """
    Format arguments for display.
    :param command: str
    :param arguments: list
    :param is_impl: boolean only show implemented
    :param is_unimpl: boolean only show unimplemented
    :param header: boolean add header
    :return: str
    """
    total_args = len(arguments)
    implemented_args = get_implemented_arguments(command)
    if is_impl:
        arguments = [arg for arg in arguments if arg.long_name in implemented_args]
    elif is_unimpl:
        arguments = [arg for arg in arguments if arg.long_name not in implemented_args]
    result = '\n'.join([
        format_option(arg)
        for arg in arguments])
    if header:
        result = format_header('Arguments', len(arguments), total_args, is_impl, is_unimpl) \
                 + '\n' \
                 + result
    return result


def format_header(what, length, total_length, is_impl, is_unimpl):
    """
    Format header string
    :param what: str
    :param length: int
    :param total_length: int
    :param is_impl: boolean
    :param is_unimpl: boolean
    :return: str
    """
    mode = 'all'
    if is_impl:
        mode = 'implemented'
    elif is_unimpl:
        mode = 'unimplemented'
    return textwrap.dedent('''
    {} ({}): {}/{}
    ------------------------------''').format(
        what,
        mode,
        length,
        total_length
    )


def check_command(command, args):
    """
    Display information about implemented and unimplemented options.
    :param command: str
    :param args: dict
    """
    implemented = get_implemented_commands()
    is_impl = args['--implemented']
    is_unimpl = args['--unimplemented']
    usage_str, help_str, commands, options, arguments = get_command_details(command)
    print(textwrap.dedent('''
    Command: [docker] {command}
    Help: {help}
    {usage}
    Subcommands: {subs}
    Implemented: {implemented}'''.format(
        command=command,
        implemented='Yes' if command in implemented else 'No',
        subs=len(commands) if commands else 'No',
        help=help_str,
        usage=usage_str
    )))

    if commands:
        print(textwrap.dedent('''
        Subcommands:
        ------------------------------'''))
        print(format_subcommands(commands))
        print()

    print(format_options(command, options, is_impl, is_unimpl))
    print(format_arguments(command, arguments, is_impl, is_unimpl))


def main():
    """
    Display information on implemented commands and options.
    :param command: str command name
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
