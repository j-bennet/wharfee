#!/usr/bin/env python
from __future__ import unicode_literals
from __future__ import print_function

import re
import sys

from optparse import OptionParser
from docker import Client
from docker.utils import kwargs_from_env
from tabulate import tabulate
from requests.exceptions import ConnectionError

from .options import COMMAND_OPTIONS

class DockerClientException(Exception):

    def __init__(self, inner_exception):
        self.inner_exception = inner_exception
        self.message = """You don't have the necessary permissions to call Docker API.
Try the following:

  # Add a docker group if it does not exist yet.
  sudo groupadd docker

  # Add the connected user "${USER}" to the docker group.
  # Change the user name to match your preferred user.
  sudo gpasswd -a ${USER} docker

  # Restart the Docker daemon.
  # If you are in Ubuntu 14.04, use docker.io instead of docker
  sudo service docker restart

You may need to reboot the machine.
"""


class DockerClient(object):

    def __init__(self):
        """
        Initialize the Docker wrapper.
        """

        self.handlers = {
            'help': (self.help, "Help on available commands."),
            'version': (self.version, "Equivalent of 'docker version'."),
            'ps': (self.containers, "Equivalent of 'docker ps'."),
            'images': (self.not_implemented, "Equivalent of 'docker images'."),
            'run': (self.not_implemented, "Equivalent of 'docker run'."),
            'stop': (self.not_implemented, "Equivalent of 'docker stop'.")
        }

        if sys.platform.startswith('darwin') \
                or sys.platform.startswith('win32'):
            # mac or win
            kwargs = kwargs_from_env()
            # hack from here:
            # http://docker-py.readthedocs.org/en/latest/boot2docker/
            kwargs['tls'].assert_hostname = False
            self.instance = Client(**kwargs)
        else:
            # unix-based
            self.instance = Client(base_url='unix://var/run/docker.sock')

    def help(self, *args, **kwargs):
        """
        Collect and return help docstrings for all commands.
        :return: iterable
        """
        _, _ = args, kwargs

        help_rows = [(key, self.handlers[key][1])
                     for key in sorted(self.handlers.keys())]
        return [tabulate(help_rows)]

    def not_implemented(self, *args, **kwargs):
        """
        Placeholder for commands to be implemented.
        :return: iterable
        """
        _, _ = args, kwargs
        return ['Not implemented.']

    def version(self, *args, **kwargs):
        """
        Print out the version. Equivalent of docker version.
        :return: iterable
        """
        _, _ = args, kwargs

        try:
            verdict = self.instance.version()
            result = []
            for k, v in verdict.iteritems():
                result.append((k, v))
            return [tabulate(result)]
        except ConnectionError as ex:
            raise DockerClientException(ex)

    def containers(self, *args, **kwargs):
        """
        Print out the list of containers. Equivalent of docker ps.
        :return: iterable
        """
        _ = args

        csdict = self.instance.containers(**kwargs)
        if len(csdict) > 0:
            return [tabulate(csdict, headers='keys')]
        else:
            return ['There are no containers to list.']

    def handle_input(self, text):
        """
        Parse the command, run it via the client, and return
        some iterable output to print out.
        :param text: user input
        :return: iterable
        """

        tokens = re.split('\s+', text) if text else ['']
        cmd = tokens[0]
        params = tokens[1:] if len(tokens) > 1 else None

        if cmd and cmd in self.handlers:
            handler = self.handlers[cmd][0]

            if params and cmd in COMMAND_OPTIONS:
                parser = OptionParser(prog=cmd, add_help_option=False)
                for opt in COMMAND_OPTIONS[cmd]:
                    parser.add_option(opt.get_option())
                popts, pargs = parser.parse_args(params)
                popts = vars(popts)
                if popts['help']:
                    return [parser.format_help()]
                else:
                    if 'help' in popts:
                        del popts['help']
                    return handler(*pargs, **popts)
            else:
                return handler(None, None)
        else:
            return self.help(None, None)
