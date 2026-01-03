# -*- coding: utf-8 -*-
import pexpect
import re
import wrappers
from importlib.metadata import distributions

from behave import given, when, then

# Pattern to match prompt with optional ANSI escape sequences
PROMPT_PATTERN = r'wharfee>\s*'


@given('we have wharfee installed')
def step_cli_installed(context):
    """
    Make sure wharfee is in installed packages.
    """
    dists = set([d.metadata['Name'].lower() for d in distributions()])
    assert 'wharfee' in dists


@when('we run wharfee')
def step_run_cli(context):
    """
    Run the process using pexpect.
    """
    context.cli = pexpect.spawnu('wharfee --no-completion')


@when('we wait for prompt')
def step_expect_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect(PROMPT_PATTERN)


@when('we send "help" command')
def step_send_help(context):
    """
    Send "help".
    """
    context.cli.sendline('help')


@when('we send "ctrl + d"')
def step_send_ctrld(context):
    """
    Send Ctrl + D to exit.
    """
    context.cli.sendcontrol('d')
    context.exit_sent = True


@when('we clear screen')
def step_send_clear(context):
    """
    Send clear.
    """
    context.cli.sendline('clear')


@when('we refresh completions')
def step_refresh(context):
    """
    Send refresh.
    """
    context.cli.sendline('refresh')


@then('we see {text} printed out')
def step_see_output(context, text):
    """
    Expect to see exact text.
    """
    patterns = list(set([text, text.strip('"')]))
    wrappers.expect_exact(context, patterns)


@then('we see {text} at line end')
def step_see_line_end(context, text):
    """
    Expect to see text and line end.
    """
    wrappers.expect_exact(context, text + '\r\n')


@then('wharfee exits')
def step_expect_exit(context):
    """
    Expect cli to exit.
    """
    context.cli.expect(pexpect.EOF)


@then('we see wharfee prompt')
def step_see_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect(PROMPT_PATTERN)


@then('we see help output')
def step_see_help(context):
    """
    Expect to see key help lines.
    """
    import pexpect as pexp
    import time

    # Help output uses a pager - collect output by paginating through
    time.sleep(0.5)
    all_output = ''
    for _ in range(10):
        try:
            chunk = context.cli.read_nonblocking(size=4096, timeout=0.3)
            all_output += chunk
        except pexp.TIMEOUT:
            pass
        context.cli.send(' ')  # space to advance pager

    # Quit pager and wait for prompt
    context.cli.send('q')
    context.cli.expect(PROMPT_PATTERN, timeout=5)
    all_output += context.cli.before

    # Strip ANSI escape codes
    output = wrappers.RE_ANSI.sub('', all_output)

    # Verify key help lines are present
    key_commands = ['attach', 'build', 'help', 'images', 'ps', 'run', 'stop']
    for cmd in key_commands:
        if cmd not in output:
            raise Exception('Expected help to contain "' + cmd + '"\n\nActual output:\n' + output)
