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
    context.has_containers = True


@when('we create container {container_name} with image {image_name}')
def step_create_container(context, container_name, image_name):
    """
    Send "create".
    """
    context.cli.sendline('create --name {0} {1}'.format(
        container_name,
        image_name))
    context.has_containers = True


@when('we start container {container_name}')
def step_start_container(context, container_name):
    """
    Send "start".
    """
    context.cli.sendline('start {0}'.format(container_name))


@when('we pause container {container_name}')
def step_pause_container(context, container_name):
    """
    Send "pause".
    """
    context.cli.sendline('pause {0}'.format(container_name))


@when('we open shell to container {name} and {path_to_shell}')
def step_shell_to_container(context, name, path_to_shell):
    """
    Send "shell".
    """
    context.cli.sendline('shell {0} {1}'.format(name, path_to_shell))


@then('we see container {container_name} paused')
def step_see_container_paused(context, container_name):
    """
    Check container is paused.
    """
    wrappers.expect_exact(context, container_name + '\r\n')
    context.cli.sendline('ps')
    wrappers.expect_exact(context, ' (Paused)')


@when('we unpause container {container_name}')
def step_unpause_container(context, container_name):
    """
    Send "unpause".
    """
    context.cli.sendline('unpause {0}'.format(container_name))


@then('we see container {container_name} unpaused')
def step_see_container_unpaused(context, container_name):
    """
    Check container is running.
    """
    wrappers.expect_exact(context, container_name + '\r\n')
    context.cli.sendline('ps')
    wrappers.expect(context, r'Up [a-zA-Z0-9\s]+\s{2,}')


@then('we see container {container_name} running')
def step_see_container_running(context, container_name):
    """
    Check container is running.
    """
    context.cli.sendline('ps')
    wrappers.expect(context,
                    r'({0}[\w \t/]*Up|Up[\w \t/]*{0})'.format(container_name))


@when('we check ports for container {container_name}')
def step_ports_container(context, container_name):
    """
    Send "port".
    """
    context.cli.sendline('port {0}'.format(container_name))


@when('we run container {container_name} with image {image_name}')
def step_run_container(context, container_name, image_name):
    """
    Send "run" with command.
    """
    context.cli.sendline('run --name {0} {1}'.format(
        container_name,
        image_name))
    context.has_containers = True


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


@when('we kill container {container_name}')
def step_kill_container(context, container_name):
    """
    Send "kill" command.
    """
    context.cli.sendline('kill {0}'.format(container_name))


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
    context.cli.sendline('attach --detach-keys=ctrl-q {0}'.format(name))


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


@then('we see {name} restarted')
def step_see_restarted(context, name):
    """
    Expect to see container name and line end.
    """
    wrappers.expect(context, '{0}\r\n'.format(name), 60)


@when('we view top for container {name}')
def step_see_top_for_container(context, name):
    """
    Send "top" command.
    """
    context.cli.sendline('top {0}'.format(name))


@then('we see top processes')
def step_see_top(context):
    """
    Expect to see [a-zA-Z0-9]+ and line end.
    """
    wrappers.expect_exact(context, 'PID')


@when('we restart container {name}')
def step_restart_container(context, name):
    """
    Send "restart" command.
    """
    context.cli.sendline('restart {0}'.format(name))


@when('we rename container {name} to {new_name}')
def step_rename_container(context, name, new_name):
    """
    Send "rename" command.
    """
    context.cli.sendline('rename {0} {1}'.format(name, new_name))
