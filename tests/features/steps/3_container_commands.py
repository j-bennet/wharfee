# -*- coding: utf-8
from __future__ import unicode_literals

import wrappers
from behave import when, then


@when('we run container {container_name} with image {image_name} and command {command} and options {options}')
def step_run_container_with_command(context, container_name, image_name, command, options):
    """
    Send "run" with command.
    """
    context.cli.sendline('run {3} --name {0} {1} {2}'.format(
        container_name,
        image_name,
        command,
        options))


@when('we run container {container_name} with image {image_name}')
def step_run_container(context, container_name, image_name):
    """
    Send "run" with command.
    """
    context.cli.sendline('run --name {0} {1}'.format(
        container_name,
        image_name))


@when('we execute {command_name} in container {container_name}')
def step_exec_command(context, command_name, container_name):
    """
    Send "run" command.
    """
    context.cli.sendline('exec {0} {1}'.format(container_name, command_name))


@when('we stop container {container_name}')
def step_stop_container(context, container_name):
    """
    Send "stop" command.
    """
    context.cli.sendline('stop {0}'.format(container_name))


@when('we remove container {name}')
def step_remove_container(context, name):
    """
    Send "rm" command.
    """
    context.cli.sendline('rm {0}'.format(name))


@then('we see {text} at line end')
def step_see_line_end(context, text):
    """
    Expect to see text and line end.
    """
    wrappers.expect_exact(context, text + '\r\n')
