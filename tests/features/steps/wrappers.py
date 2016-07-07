# -*- coding: utf-8
import re


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
        # Strip color codes out of the output.
        actual = re.sub(r'\x1b\[([0-9A-Za-z;?])+[m|K]?', '', context.cli.before)
        raise Exception('Expected:\n---\n{0}\n---\n\nActual:\n---\n{1}\n---'.format(
            expected,
            actual))
