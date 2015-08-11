from __future__ import unicode_literals
from __future__ import print_function

import pytest
import shlex
from optparse import OptionError
from textwrap import dedent
from wharfee.options import parse_command_options, format_command_help, \
    format_command_line
from wharfee.completer import DockerCompleter


@pytest.mark.parametrize("help_opt_name", [
    '-h',
    '--help'
])
def test_parse_images_help(help_opt_name):
    """
    Test parsing of a "--help"
    """
    parser, popts, pargs = parse_command_options('images', [help_opt_name])
    assert popts['help'] is True


def test_parse_run():
    """
    Test parsing of a simple "run"
    """
    parser, popts, pargs = parse_command_options(
        'run', ['--name', 'boo', 'ubuntu'])
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
    input = ('run -d ubuntu:14.04 /bin/sh -c '
             '"while true; do echo hello world; sleep 1; done"')
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
        'tty': False,
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
    for expected_key in expected_opts:
        assert expected_key in popts
        assert popts[expected_key] == expected_opts[expected_key]


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


def test_help_formatting():
    """
    Format and output help for the command.
    """
    output = dedent(format_command_help('rmi')).strip()

    expected = dedent("""
        Usage: rmi [options] image

        Options:
          -h, --help        Display help for this command.

          Non-standard options:
            --all-dangling  Shortcut to remove all dangling images.
    """).strip()

    print(output)

    assert output == expected


@pytest.mark.parametrize('text, is_long, expected', [
    ('exec -it boo /usr/bin/bash', False, 'exec -i -t boo /usr/bin/bash'),
    ('exec -i -t boo /usr/bin/bash', False, 'exec -i -t boo /usr/bin/bash'),
    ('exec -i -t boo /usr/bin/bash', True, 'exec --interactive --tty boo /usr/bin/bash'),
    ('exec --interactive --tty boo /usr/bin/bash', False, 'exec -i -t boo /usr/bin/bash'),
    ('exec -i --tty boo /usr/bin/bash', False, 'exec -i -t boo /usr/bin/bash'),
    (('run --name some-percona --env MYSQL_ROOT_PASSWORD=masterkey '
      '--publish 9999:3306 --interactive --tty percona'),
     False,
     ('run --name=some-percona -e MYSQL_ROOT_PASSWORD=masterkey '
      '-p=9999:3306 -i -t percona')),
    ('run -e TWO_ENVS="boo hoo" -e ONE_VAR=foo -i -t some-image',
     False,
     'run -e TWO_ENVS="boo hoo" -e ONE_VAR=foo -i -t some-image')
])
def test_external_command_line(text, is_long, expected):
    """
    Parse and reconstruct the command line.
    """
    cmd, params = text.split(' ', 1)
    params = shlex.split(params)

    parser, popts, pargs = parse_command_options(cmd, params)

    result = format_command_line(cmd, is_long, pargs, popts)

    result_words = set(result.split(' ')[1:])
    expected_words = set(expected.split(' '))

    assert result_words == expected_words
