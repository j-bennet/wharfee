# -*- coding: utf-8
from __future__ import unicode_literals
from behave import when


@when('we ask for docker {something}')
def step_info(context, something):
    """
    Send one-word command (info, version).
    """
    context.cli.sendline('{0}'.format(something))
