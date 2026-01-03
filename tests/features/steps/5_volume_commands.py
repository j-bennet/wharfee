# -*- coding: utf-8
from behave import when


@when('we list volumes')
def step_volume_ls(context):
    """
    Send volume ls.
    """
    context.cli.sendline('volume ls')


@when('we create volume {name}')
def step_volume_create(context, name):
    """
    Send volume create.
    """
    context.cli.sendline('volume create --name {0}'.format(name))


@when('we inspect volume {name}')
def step_volume_inspect(context, name):
    """
    Send volume inspect.
    """
    context.cli.sendline('volume inspect {0}'.format(name))


@when('we remove volume {name}')
def step_volume_rm(context, name):
    """
    Send volume create.
    """
    context.cli.sendline('volume rm {0}'.format(name))
