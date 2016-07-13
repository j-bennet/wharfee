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


@when('we force remove container {name}')
def step_force_remove_container(context, name):
    """
    Send "rm -f" command.
    """
    context.cli.sendline('rm -f {0}'.format(name))


@when('we attach to container {name}')
def step_attach_container(context, name):
    """
    Send "attach" command.
    """
    context.cli.sendline('attach --detach-keys ctrl-q {0}'.format(name))


@when('we detach from container {name}')
def step_detach_container(context, name):
    """
    Send detach keys command.
    """
    context.cli.sendcontrol('q')


@when('we see logs for container {name}')
def step_see_logs(context, name):
    """
    Send "logs" command.
    """
    context.cli.sendline('logs {0}'.format(name))


@when('we remove stopped containers')
def step_remove_stopped(context):
    """
    Send "rm" command.
    """
    context.cli.sendline('rm --all-stopped')


@when('we list containers')
def step_list_containers(context):
    """
    Send "ps" command.
    """
    context.cli.sendline('ps')


@then('we see id string')
def step_see_id_string(context):
    """
    Expect to see [a-zA-Z0-9]+ and line end.
    """
    wrappers.expect(context, '[a-zA-Z0-9]+\r\n')


@then('we see {text} at line end')
def step_see_line_end(context, text):
    """
    Expect to see text and line end.
    """
    wrappers.expect_exact(context, text + '\r\n')
