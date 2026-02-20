import os
import pytest
from prompt_toolkit.completion import Completion
from prompt_toolkit.document import Document
from wharfee.options import all_options
from wharfee.options import COMMAND_NAMES
from mock import patch


def completion_to_tuple(c):
    """Convert Completion to hashable tuple for comparison."""
    return (c.text, c.start_position)


def completions_to_set(completions):
    """Convert list of Completions to set of tuples for comparison."""
    return set(completion_to_tuple(c) for c in completions)


def expected_completions_set(texts, start_position=0):
    """Create expected set of completion tuples."""
    return set((t, start_position) for t in texts)


@pytest.fixture
def completer():
    import wharfee.completer as cmp
    return cmp.DockerCompleter()


@pytest.fixture
def complete_event():
    from mock import Mock
    return Mock()

cs1 = ['newton', 'tesla', 'einstein', 'edison']
rs1 = ['einstein', 'edison']
im1 = ['ubuntu', 'hello-world', 'postgres', 'nginx']

cs2 = ['desperate_hodgkin', 'desperate_torvalds', 'silly_fermat', 'some-percona']


def test_empty_string_completion(completer, complete_event):
    """
    In the beginning of the line, all available commands are suggested.
    """
    text = ''
    position = 0
    result = completions_to_set(completer.get_completions(
        Document(text=text, cursor_position=position),
        complete_event))
    assert result == expected_completions_set(COMMAND_NAMES, 0)


def test_build_path_completion_absolute(completer, complete_event):
    """
    Suggest build paths from filesystem root.
    """
    command = 'build /'

    position = len(command)

    with patch('wharfee.completer.list_dir',
               return_value=['etc', 'home', 'tmp', 'usr', 'var']):

        result = completions_to_set(completer.get_completions(
            Document(text=command, cursor_position=position),
            complete_event))

        expected = expected_completions_set(['etc', 'home', 'tmp', 'usr', 'var'], 0)

        assert expected.issubset(result)


def test_build_path_completion_user(completer, complete_event):
    """
    Suggest build paths from user home directory.
    """
    command = 'build ~'

    position = len(command)

    with patch('wharfee.completer.list_dir',
               return_value=['Documents', 'Downloads', 'Pictures']):

        result = completions_to_set(completer.get_completions(
            Document(text=command, cursor_position=position),
            complete_event))

        expected_texts = ['~{0}{1}'.format(os.path.sep, d) for d in ['Documents', 'Downloads']]
        expected = expected_completions_set(expected_texts, -1)

        assert expected.issubset(result)


def test_build_path_completion_user_dir(completer, complete_event):
    """
    Suggest build paths from user home directory.
    """
    command = 'build ~/s'

    position = len(command)

    with patch('wharfee.completer.list_dir',
               return_value=['.config', 'db-dumps', 'src', 'venv']):

        result = completions_to_set(completer.get_completions(
            Document(text=command, cursor_position=position),
            complete_event))

        expected = expected_completions_set(['src'], -1)

        assert expected.issubset(result)


@pytest.mark.parametrize("command, expected", [
    ("h", ['help']),
    ("he", ['help']),
    ("hel", ['help']),
    ("help", ['help']),
    ('run -d ubuntu:14.04 /bin/sh -c "w', [])  # not complete in quoted string
])
def test_command_completion(completer, complete_event, command, expected):
    """
    Test command suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    position = len(command)
    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position),
        complete_event))

    expected = expected_completions_set(expected, -len(command))

    assert result == expected


@pytest.mark.parametrize("command, expected", [
    ("h", ['help', 'shell', 'push', 'attach', 'search', 'refresh']),
    ("he", ['help', 'shell']),
    ("hel", ['help', 'shell']),
    ("help", ['help']),
    ('run -d ubuntu:14.04 /bin/sh -c "w', [])  # not complete in quoted string
])
def test_command_completion_fuzzy(completer, complete_event, command, expected):
    """
    Test command suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    completer.set_fuzzy_match(True)

    position = len(command)
    result = list(completer.get_completions(
        Document(text=command, cursor_position=position),
        complete_event))

    expected = list(map(lambda t: Completion(t, -len(command)), expected))

    assert result == expected


pso = list(filter(lambda x: x.name.startswith('-'), all_options('ps')))


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("ps ", pso, 0),
    ("ps --", list(filter(
        lambda x: x.long_name and x.long_name.startswith('--'), pso)), -2),
    ("ps --h", list(filter(
        lambda x: x.long_name and x.long_name.startswith('--h'), pso)), -3),
    ("ps --all ", list(filter(
        lambda x: x.long_name not in ['--all'], pso)), 0),
    ("ps --all --quiet ", list(filter(
        lambda x: x.long_name not in ['--all', '--quiet'], pso)), 0),
])
def test_options_completion_long(completer, complete_event, command, expected, expected_pos):
    """
    Test command options suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    position = len(command)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = expected_completions_set(
        [t.get_name(is_long=True) for t in expected], expected_pos)

    assert result == expected


def option_map(cmd, is_long):
    result = {}
    for x in all_options(cmd):
        if x.name.startswith('-'):
            result[x.get_name(is_long)] = x.display
    return result


psm = option_map('ps', True)


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("ps ", sorted(psm.keys()), 0),
    ("ps h", ['--help'], -1),
    ("ps i", ['--since', '--size', '--quiet'], -1),
    ("ps ze", ['--size'], -2),
])
def test_options_completion_long_fuzzy(completer, complete_event, command, expected, expected_pos):
    """
    Test command options suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    completer.set_fuzzy_match(True)

    position = len(command)

    result = list(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = list(map(lambda t: Completion(
        t, expected_pos, psm[t]), expected))

    assert result == expected


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("ps ", pso, 0),
    ("ps -", list(filter(
        lambda x: x.name.startswith('-'), pso)), -1),
    ("ps -h", list(filter(
        lambda x: x.short_name and x.short_name.startswith('-h'), pso)), -2),
])
def test_options_completion_short(completer, complete_event, command, expected,
                                  expected_pos):
    """
    Test command options suggestions.
    :param command: string: text that user started typing
    :param expected: list: expected completions
    """
    completer.set_long_options(False)

    position = len(command)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = expected_completions_set(
        [t.get_name(is_long=completer.get_long_options()) for t in expected],
        expected_pos)

    assert result == expected


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("ps --before ", cs1, 0),
    ("ps --before e", list(filter(lambda x: x.startswith('e'), cs1)), -1),
    ("ps --before ei", list(filter(lambda x: x.startswith('ei'), cs1)), -2),
])
def test_options_container_completion(completer, complete_event, command,
                                      expected, expected_pos):
    """
    Suggest container names in relevant options (ps --before)
    """
    completer.set_containers(cs1)

    position = len(command)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = expected_completions_set(expected, expected_pos)

    assert result == expected


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("top ", list(map(
        lambda x: (x, x), rs1)) + [('--help', '-h/--help')], 0),
    ("top e", list(map(
        lambda x: (x, x), filter(lambda x: x.startswith('e'), rs1))), -1),
])
def test_options_container_running_completion(completer, complete_event,
                                              command, expected, expected_pos):
    """
    Suggest running container names (top [container])
    """
    completer.set_containers(cs1)
    completer.set_running(rs1)

    position = len(command)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected_set = set((text, expected_pos) for text, display in expected)

    assert result == expected_set


@pytest.mark.parametrize("command, expected, expected_pos", [
    ("rm ", ['--all', '--all-stopped', ('--force', '-f/--force'), ('--help', '-h/--help')] + cs2, 0),
    ("rm spe", ['--all-stopped', 'desperate_hodgkin', 'desperate_torvalds',
                'some-percona'], -3),
])
def test_options_container_completion_fuzzy(completer, complete_event, command,
                                            expected, expected_pos):
    """
    Suggest running container names (top [container])
    """
    completer.set_containers(cs2)

    completer.set_fuzzy_match(True)

    position = len(command)

    result = list(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected_completions = []
    for x in expected:
        if isinstance(x, tuple):
            expected_completions.append(Completion(x[0], expected_pos, x[1]))
        else:
            expected_completions.append(Completion(x, expected_pos))

    assert result == expected_completions


def test_options_image_completion(completer, complete_event):
    """
    Suggest image names in relevant options (images --filter)
    """
    command = 'images --filter '
    expected = ['ubuntu', 'hello-world', 'postgres', 'nginx']
    expected_pos = 0

    completer.set_images(expected)
    position = len(command)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = expected_completions_set(expected, expected_pos)

    assert result == expected


@pytest.mark.parametrize("command, expected, expected_pos", [
    ('images --filter ', ['hello-world', 'nginx', 'postgres', 'ubuntu'], 0),
    ('images --filter n', ['nginx', 'ubuntu'], -1),
    ('images --filter g', ['nginx', 'postgres'], -1),
    ('images --filter u', ['ubuntu'], -1),
])
def test_options_image_completion_fuzzy(completer, complete_event, command,
                                        expected, expected_pos):
    """
    Suggest image names in relevant options (images --filter)
    """
    completer.set_images(im1)

    completer.set_fuzzy_match(True)

    position = len(command)

    result = list(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = list(map(lambda t: Completion(t, expected_pos), expected))

    assert result == expected


@pytest.mark.parametrize("command, expected, expected_pos", [
    ('volume create ', [('--name',), ('--help', '-h/--help'),
                        ('--opt', '-o/--opt'), ('--driver', '-d/--driver')], 0),
    ('volume rm ', [('--help', '-h/--help'), ('abc',), ('def',)], 0),
    ('volume ls ', [('--help', '-h/--help'), ('--filter',),
                    ('--quiet', '-q/--quiet')], 0),
    ('volume inspect ', [('--help', '-h/--help'), ('abc',), ('def',)], 0),
])
def test_options_volume_completion(completer, complete_event, command,
                                   expected, expected_pos):
    """
    Suggest options in volume commands
    """
    position = len(command)

    completer.set_volumes(['abc', 'def'])

    completer.set_fuzzy_match(True)

    result = completions_to_set(completer.get_completions(
        Document(text=command, cursor_position=position), complete_event))

    expected = expected_completions_set([t[0] for t in expected], expected_pos)

    assert result == expected
