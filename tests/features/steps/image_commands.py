# -*- coding: utf-8
from __future__ import unicode_literals

from behave import when, then


@when('we build {image_name} from Dockerfile')
def step_build_dockerfile(context, image_name):
    """
    Send "build -t test-image ./tests/features/fixture_data/".
    """
    context.cli.sendline('build -t {0} {1}'.format(image_name, context.data_dir))


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


@when('we log in as {user} with {password}')
def step_log_in(context, user, password):
    """
    Send "login" command.
    """
    context.cli.sendline('login -u {0} -p {1}'.format(user, password))


@then('we see login success')
def step_see_log_in_success(context):
    """
    Expect to see login succeeded.
    """
    context.cli.expect_exact('Login Succeeded', timeout=30)


@when('we tag {image_name} into {repo_name}')
def step_tag_image(context, image_name, repo_name):
    """
    Send "tag" command.
    """
    context.cli.sendline('tag {0} {1}'.format(image_name, repo_name))


@then('we see {image_name} tagged into {repo_name}')
def step_see_image_tagged(context, image_name, repo_name):
    """
    Expect to see image tagged.
    """
    context.cli.expect_exact('Tagged {0} into {1}'.format(image_name, repo_name))


@when('we remove image {image_name}')
def step_remove_image(context, image_name):
    """
    Send "rmi" command.
    """
    context.cli.sendline('rmi {0}'.format(image_name))


@then('we see image {image_name} removed')
def step_see_image_removed(context, image_name):
    """
    Expect to see image removed.
    """
    context.cli.expect_exact(image_name)


@when('we list images')
def step_list_images(context):
    """
    Send "images" command.
    """
    context.cli.sendline('images')


@then('we see image {image_name} listed')
def step_see_image_listed(context, image_name):
    """
    Expect to see image listed.
    """
    context.cli.expect_exact('hello-world')


@when('we inspect {name}')
def step_inspect(context, name):
    """
    Send "inspect" command.
    """
    context.cli.sendline('inspect {0}'.format(name))


@when('we search for {name}')
def step_search(context, name):
    """
    Send "search" command.
    """
    context.cli.sendline('search {0}'.format(name))


@then('we see {text} output')
def step_see_output(context, text):
    """
    Expect to see ouptut.
    """
    context.cli.expect_exact([text, text.strip('"')])
