# -*- coding: utf-8
from __future__ import unicode_literals

import wrappers
from behave import when, then


@when('we run container {container_name} with image {image_name}')
def step_run_container(context, container_name, image_name):
    """
    Send "run" command.
    """
    context.cli.sendline('run --name {0} {1}'.format(container_name, image_name))


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
