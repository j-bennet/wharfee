# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

"""
Helpers to connect to docker.
"""

import sys

from docker import AutoVersionClient
from docker.utils import kwargs_from_env


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
