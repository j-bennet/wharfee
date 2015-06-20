# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pip
import pexpect

from behave import given, when, then

@given('we have dockercli installed')
def step_impl(context):
    ds = set([di.key for di in pip.get_installed_distributions()])
    assert 'dockercli' in ds

@when('we run dockercli')
def step_impl(context):
    context.cli = pexpect.spawnu('dockercli')

@when('we wait for prompt')
def step_impl(context):
    context.cli.expect('dockercli> ')

@when('we send "help" command')
def step_impl(context):
    context.cli.sendline('help')

@when('we send "ctrl + d"')
def step_impl(context):
    context.cli.sendcontrol('d')
    context.exit_sent = True

@then('dockercli exits')
def step_impl(context):
    context.cli.expect(pexpect.EOF)

@then('we see dockercli prompt')
def step_impl(context):
    context.cli.expect('dockercli> ')

@then('we see help output')
def step_impl(context):
    for expected_line in context.fixture_lines['help.txt']:
        context.cli.expect_exact(expected_line)
