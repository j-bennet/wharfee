# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

import os
import sys
import pexpect
import codecs

from docker import AutoVersionClient
from docker.utils import kwargs_from_env


def read_fixture_lines(filename):
    """
    Read lines of text from file.
    :param filename: string name
    :return: list of strings
    """
    lines = []
    for line in codecs.open(filename, 'r', encoding='utf-8'):
        lines.append(line.strip())
    return lines


def read_fixture_files():
    """
    Read all files inside fixture_data directory.
    """
    fixture_dict = {}

    current_dir = os.path.dirname(__file__)
    fixture_dir = os.path.join(current_dir, 'fixture_data/')
    for filename in os.listdir(fixture_dir):
        if filename not in ['.', '..']:
            fullname = os.path.join(fixture_dir, filename)
            fixture_dict[filename] = read_fixture_lines(fullname)

    return fixture_dict


def init_docker_client(timeout=2):
    """
    Init docker-py client.
    """
    if sys.platform.startswith('darwin') \
            or sys.platform.startswith('win32'):
        # mac or win
        kwargs = kwargs_from_env()
        kwargs['tls'].assert_hostname = False
        kwargs['timeout'] = timeout
        client = AutoVersionClient(**kwargs)
    else:
        # unix-based
        client = AutoVersionClient(
            timeout=timeout,
            base_url='unix://var/run/docker.sock')
    return client


def pull_required_images(client):
    """
    Make sure we have busybox image pulled.
    :param client: AutoVersionClient
    """
    for line in client.pull('busybox:latest', stream=True):
        print(line)


def before_all(context):
    """
    Set env parameters.
    """
    os.environ['LINES'] = "50"
    os.environ['COLUMNS'] = "120"
    context.fixture_lines = read_fixture_files()
    context.client = init_docker_client()
    pull_required_images(context.client)
    context.exit_sent = False


def after_scenario(context, _):
    """
    Cleans up after each test complete.
    """

    if hasattr(context, 'cli') and not context.exit_sent:
        # Send Ctrl + D into cli
        context.cli.sendcontrol('d')
        context.cli.expect(pexpect.EOF)
