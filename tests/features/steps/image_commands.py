# -*- coding: utf-8
from __future__ import unicode_literals

from behave import when, then


@when('we build image from Dockerfile')
def step_build_dockerfile(context):
    """
    Send "build -t test-image ./tests/features/fixture_data/".
    """
    context.cli.sendline('build -t test-image ' + context.data_dir)


@then('we see image built')
def step_see_image_built(context):
    """
    Expect to see image built.
    """
    context.cli.expect('Successfully built')
