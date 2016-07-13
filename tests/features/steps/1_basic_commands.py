# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pip
import pexpect
import wrappers

from behave import given, when, then


@given('we have wharfee installed')
def step_cli_installed(context):
    """
    Make sure wharfee is in installed packages.
    """
    dists = set([di.key for di in pip.get_installed_distributions()])
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
    context.cli.expect_exact('wharfee> ')


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
    wrappers.expect_exact(context, 'wharfee> ')


@then('we see help output')
def step_see_help(context):
    """
    Expect to see help lines.
    """
    for expected_line in context.fixture_lines['help.txt']:
        try:
            context.cli.expect_exact(expected_line, timeout=1)
        except Exception:
            raise Exception('Expected: ' + expected_line)
