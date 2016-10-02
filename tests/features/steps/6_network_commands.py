# -*- coding: utf-8
from __future__ import unicode_literals

import wrappers
from behave import when, then


@when('we create network {name}')
def step_create_network(context, name):
    """
    Send "network create".
    """
    context.cli.sendline('network create {0}'.format(name))


@when('we remove network {name}')
def step_remove_network(context, name):
    """
    Send "network rm" command.
    """
    context.cli.sendline('network rm {0}'.format(name))
