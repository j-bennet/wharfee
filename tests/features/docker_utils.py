# -*- coding: utf-8 -*-
"""
Helpers to connect to docker.
"""

import sys

from docker import APIClient as DockerAPIClient
from docker.utils import kwargs_from_env


def init_docker_client(timeout=2):
    """
    Init docker-py client.
    """
    if sys.platform.startswith('darwin') \
            or sys.platform.startswith('win32'):
        # mac or win
        kwargs = kwargs_from_env()
        if 'tls' in kwargs:
            kwargs['tls'].assert_hostname = False
        kwargs['timeout'] = timeout
        client = DockerAPIClient(**kwargs)
    else:
        # unix-based
        client = DockerAPIClient(
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
