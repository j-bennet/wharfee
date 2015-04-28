from __future__ import unicode_literals

import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document
from dockercli.options import COMMAND_OPTIONS
from dockercli.options import COMMAND_NAMES


@pytest.fixture
def completer():
    import dockercli.completer as cmp
    return cmp.DockerCompleter()


@pytest.fixture
def complete_event():
    from mock import Mock
    return Mock()


def test_empty_string_completion(completer, complete_event):
    """
    In the beginning of the line, all available commands are suggested.
    """
    text = ''
    position = 0
    result = set(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))
    assert result == set(map(Completion, COMMAND_NAMES))


def test_matching_command_completion(completer, complete_event):
    """
    Beginning of the command should suggest the command.
    """
    _test_command_completion(completer, complete_event, 'h', 'help')
    _test_command_completion(completer, complete_event, 'he', 'help')
    _test_command_completion(completer, complete_event, 'hel', 'help')
    _test_command_completion(completer, complete_event, 'help', 'help')

    _test_command_completion(completer, complete_event, 'i', 'images')
    _test_command_completion(completer, complete_event, 'im', 'images')
    _test_command_completion(completer, complete_event, 'ima', 'images')
    _test_command_completion(completer, complete_event, 'imag', 'images')


def test_options_completion(completer, complete_event):
    """
    After command name, suggest command options.
    """

    ps_opts = _get_command_option_names('ps')

    _test_options_completion(
        completer, complete_event, 'ps ', ps_opts, 0)

    _test_options_completion(
        completer, complete_event, 'ps --', [n for n in ps_opts if n.startswith('--')], -2)

    _test_options_completion(
        completer, complete_event, 'ps --h', ['--help'], -3)


def test_options_completion_exclusion(completer, complete_event):
    """
    After command name, do not suggest options that are already set.
    """

    ps_opts = _get_command_option_names('ps')

    _test_options_completion(
        completer,
        complete_event,
        'ps --all ',
        [n for n in ps_opts if n != '--all'],
        0)

    _test_options_completion(
        completer,
        complete_event,
        'ps --all --quiet ',
        [n for n in ps_opts if n not in ['--all', '--quiet']],
        0)


def test_options_container_completion(completer, complete_event):
    """
    Suggest container names in relevant options (ps --before)
    """
    container_names = ['newton', 'tesla', 'einstein']
    image_names = ['ubuntu', 'ubuntu:12.04', 'ubuntu:14.04']

    completer.set_containers(container_names)
    completer.set_images(image_names)

    _test_options_completion(
        completer,
        complete_event,
        'ps --before ',
        container_names,
        0
    )

def _get_command_option_names(command):
    """
    Helper method to get all option names for command.
    :param command: string
    :return: list
    """
    return [opt.name for opt in COMMAND_OPTIONS[command]]


def _test_command_completion(completer, complete_event, command, expected):
    """
    Helper method to test command suggestions.
    :param command: string: text that user started typing
    :param expected: string: expected completion
    """
    position = len(command)
    result = set(completer.get_completions(
        Document(text=command, cursor_position=position),
        complete_event))
    assert result == {Completion(expected, -len(command))}


def _test_options_completion(completer, complete_event, command, expected, expected_pos):
    """
    Helper method to test command options suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    position = len(command)

    result = set(completer.get_completions(
        Document(text=command, cursor_position=position),
        complete_event))

    expected = set(map(lambda t: Completion(t, expected_pos), expected))

    assert result == expected
