# -*- coding: utf-8 -*-
import os
import pexpect
from behave import given, when, then

def read_fixture_lines(filename):
    """
    Read text from file.
    :param filename: string name
    :return: list
    """
    current_dir = os.path.dirname(__file__)
    filename = os.path.join(current_dir, 'fixture_data/', filename)
    lines = open(filename, 'r').readlines()
    return lines

@given('we have dockercli installed')
def step_impl(context):
    pass

@when('we run dockercli')
def step_impl(context):
    context.cli = pexpect.spawn('dockercli')

@when('we send "help" command')
def step_impl(context):
    context.cli.expect('dockercli> ')
    context.cli.sendline('help')

@then('we see dockercli prompt')
def step_impl(context):
    context.cli.expect('dockercli> ')

@then('we see help output')
def step_impl(context):
    lines = read_fixture_lines('help.txt')
    for line in lines:
        print('expecting', line)
        context.cli.expect_exact(line)
