# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pip
import pexpect

from behave import given, when, then


@given('we have dockercli installed')
def step_cli_installed(context):
    """
    Make sure dockercli is in installed packages.
    """
    dists = set([di.key for di in pip.get_installed_distributions()])
    assert 'dockercli' in dists


@when('we run dockercli')
def step_run_cli(context):
    """
    Run the process using pexpect.
    """
    context.cli = pexpect.spawnu('dockercli')


@when('we wait for prompt')
def step_expect_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect('dockercli> ')


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


@then('dockercli exits')
def step_expect_exit(context):
    """
    Expect cli to exit.
    """
    context.cli.expect(pexpect.EOF)


@then('we see dockercli prompt')
def step_see_prompt(context):
    """
    Expect to see prompt.
    """
    context.cli.expect('dockercli> ')


@then('we see help output')
def step_see_help(context):
    """
    Expect to see help lines.
    """
    for expected_line in context.fixture_lines['help.txt']:
        context.cli.expect_exact(expected_line)
