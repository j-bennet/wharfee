from __future__ import unicode_literals
from __future__ import print_function

import pytest
import shlex
from optparse import OptionError
from dockercli.options import parse_command_options
from dockercli.completer import DockerCompleter


@pytest.mark.parametrize("help_opt_name", [
    '-h',
    '--help'
])


def test_parse_images_help(help_opt_name):
    """
    Test parsing of a "--help"
    """
    parser, popts, pargs = parse_command_options('images', [help_opt_name])
    assert popts['help'] == True


def test_parse_run():
    """
    Test parsing of a simple "run"
    """
    parser, popts, pargs = parse_command_options('run', ['--name', 'boo', 'ubuntu'])
    assert pargs == ['ubuntu']
    assert popts['name'] == 'boo'


def test_parse_run_command():
    """
    Test parsing of a "run" with command to run
    """
    parser, popts, pargs = parse_command_options(
        'run',
        ['--name', 'boo', 'ubuntu', 'top'])
    assert pargs == ['ubuntu', 'top']
    assert popts['name'] == 'boo'


def test_parse_run_command_string():
    """
    Test parsing of a "run" with command to run and parameter, quoted
    """
    parser, popts, pargs = parse_command_options(
        'run',
        ['--name', 'boo', 'ubuntu', 'top -b'])
    assert pargs == ['ubuntu', 'top -b']
    assert popts['name'] == 'boo'


def test_parse_run_command_with_dash_arg():
    """
    Test parsing of a "run" with command to run and parameter, unquoted
    """
    parser, popts, pargs = parse_command_options(
        'run',
        ['--name', 'boo', 'ubuntu', 'top', '-b'])
    assert pargs == ['ubuntu', 'top', '-b']
    assert popts['name'] == 'boo'


def test_parse_quoted_string():
    """
    Test parsing of a "complicated" run command.
    """
    input = 'run -d ubuntu:14.04 /bin/sh -c "while true; do echo hello world; sleep 1; done"'
    first = DockerCompleter.first_token(input)
    assert first == 'run'


def test_parse_quoted_string_start():
    """
    Test parsing of a "complicated" run command.
    """
    input = 'run -d ubuntu:14.04 /bin/sh -c "w'
    first = DockerCompleter.first_token(input)
    assert first == 'run'

def test_parse_multiple_args():
    """
    Parsing multiple -e options to "run".
    :return:
    """
    expected_opts = {
        'tty': None,
        'help': None,
        'remove': None,
        'environment': [u'FOO=1', u'BOO=2'],
        'detach': None,
        'name': u'boo'
    }

    expected_args = ['ubuntu']

    parser, popts, pargs = parse_command_options(
        'run',
        ['--name', 'boo', '-e', 'FOO=1', '-e', 'BOO=2', 'ubuntu'])

    assert pargs == expected_args
    assert popts == expected_opts

def test_parse_multiple_args_without_equal():
    """
    Parsing multiple -e options to "run".
    :return:
    """
    text = 'run --name boo -e FOO 1 -e BOO 2 ubuntu'
    tokens = shlex.split(text) if text else ['']
    cmd = tokens[0]
    params = tokens[1:]

    with pytest.raises(OptionError) as ex:
        parse_command_options(cmd, params)
        assert 'KEY=VALUE' in ex.message
