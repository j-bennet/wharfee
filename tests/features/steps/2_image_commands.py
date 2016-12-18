# -*- coding: utf-8
from __future__ import unicode_literals

import wrappers
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
    wrappers.expect_exact(context, 'Successfully built')


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
    wrappers.expect_exact(context, [
        'Downloaded newer image for ' + image_name,
        'Image is up to date for ' + image_name,
        'Pull complete',
        'Download complete'],
        timeout=180)


@when('we log in as {user}, {email} with {password}')
def step_log_in(context, user, email, password):
    """
    Send "login" command.
    """
    context.cli.sendline('login -u {0} -e {1} -p {2}'.format(user, email, password))


@then('we see login success')
def step_see_log_in_success(context):
    """
    Expect to see login succeeded.
    """
    wrappers.expect_exact(context, 'Login Succeeded', 30)


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
    wrappers.expect_exact(context, 'Tagged {0} into {1}'.format(image_name, repo_name))


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
    wrappers.expect_exact(context, image_name)


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
    wrappers.expect_exact(context, 'hello-world')


@when('we inspect image {name}')
def step_inspect_image(context, name):
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
