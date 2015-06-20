# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pexpect

from behave import given, when, then

@given('we have dockercli installed')
def step_impl(context):
    pass

@when('we run dockercli')
def step_impl(context):
    context.cli = pexpect.spawnu('dockercli')

@when('we send "help" command')
def step_impl(context):
    context.cli.expect('dockercli> ')
    context.cli.sendline('help')

@then('we see dockercli prompt')
def step_impl(context):
    context.cli.expect('dockercli> ')

@then('we see help output')
def step_impl(context):
    for expected_line in context.fixture_lines['help.txt']:
        context.cli.expect_exact(expected_line)
