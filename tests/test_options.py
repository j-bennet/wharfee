from __future__ import unicode_literals
from __future__ import print_function

from dockercli.options import parse_command_options


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
