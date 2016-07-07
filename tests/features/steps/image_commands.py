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
    context.cli.expect_exact('Successfully built')


@when('we pull {image_name} image')
def step_pull_image(context, image_name):
    """
    Send "pull {image_name}".
    """
    context.cli.sendline('pull ' + image_name)


@then('we see {image_name} pulled')
def step_see_image_pulled(context, image_name):
    """
    Expect to see image pulled.
    """
    context.cli.expect_exact([
        'Downloaded newer image for ' + image_name,
        'Image is up to date for ' + image_name
    ])
