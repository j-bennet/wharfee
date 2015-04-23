from __future__ import unicode_literals
import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document


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
    assert result == set(map(Completion, completer.commands))


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
    _test_options_completion(
        completer, complete_event, 'ps ', ['--help', '--all', '--quiet', '--latest', '--size'], 0)

    _test_options_completion(
        completer, complete_event, 'ps --', ['--help', '--all', '--quiet', '--latest', '--size'], -2)

    _test_options_completion(
        completer, complete_event, 'ps --h', ['--help'], -3)


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
