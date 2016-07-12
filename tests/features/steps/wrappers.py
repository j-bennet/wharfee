# -*- coding: utf-8
import re

RE_ANSI = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')


def expect(context, expected, timeout=30):
    """
    Wrapper for pexpect's expect with clear output logging.
    :param context:
    :param expected:
    :param timeout:
    """
    try:
        context.cli.expect(expected, timeout=timeout)
    except:
        handle_exception(context, expected)


def expect_exact(context, expected, timeout=30):
    """
    Wrapper for pexpect's expect exact with clear output logging.
    :param context:
    :param expected:
    :param timeout:
    """
    try:
        context.cli.expect_exact(expected, timeout=timeout)
    except:
        handle_exception(context, expected)


def handle_exception(context, expected):
    # Strip color codes out of the output.
    lines = context.cli.before.split('\r\n')
    actual_lines = [RE_ANSI.sub('', l).rstrip() for l in lines]
    actual = '\r\n'.join([l for l in actual_lines if l != ''])
    raise Exception('Expected:\n---\n{0}\n---\n\nActual:\n---\n{1}\n---'.format(
        expected,
        actual))
