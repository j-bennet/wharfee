from __future__ import unicode_literals
from __future__ import print_function

import os
import pytest
from time import sleep
from wharfee.formatter import format_data
from wharfee.formatter import format_struct
from wharfee.formatter import format_top
from wharfee.formatter import format_port_lines
from wharfee.formatter import JsonStreamFormatter


@pytest.mark.parametrize("data, expected", [
    ([{'HostPort': '8888', 'HostIp': '0.0.0.0'}],
     ["0.0.0.0:8888"]),
    ({u'80/tcp': [{u'HostPort': u'8888', u'HostIp': u'0.0.0.0'}]},
     ["80/tcp->0.0.0.0:8888"])
])
def test_ports_formatting(data, expected):
    """
    Test ports formatting
    """
    result = format_port_lines(data)
    assert result == expected


def test_top_formatting():
    """
    Test formatting of top output.
    """
    data = {
        u'Processes': [
            [u'root', u'27390', u'2347', u'0', u'Jun02', u'?', u'00:00:21',
             u'/bin/sh -c while true; do echo Hello boo; sleep 1; done'],
            [u'root', u'32694', u'27390', u'0', u'21:52', u'?', u'00:00:00',
             u'sleep 1']],
        u'Titles': [u'UID', u'PID', u'PPID', u'C', u'STIME', u'TTY', u'TIME',
                    u'CMD']
    }
    formatted = format_top(data)
    print('\n')
    print('\n'.join(formatted))


@pytest.mark.skipif(True, reason='Long running.')
def test_json_stream_formatting():
    """
    Test formatting of pull output
    """
    print("\n")
    fmt = JsonStreamFormatter(pull_stream())
    fmt.output()


def pull_stream():
    """
    Read pull output line by line.
    """
    p = os.path.dirname(os.path.realpath(__file__))
    f = os.path.join(p, 'data/pull.output')
    for line in open(f, 'r'):
        line = line.strip()
        sleep(0.1)
        yield line if line else '{}'


def test_ps_data_formatting():
    """
    Test formatting for list of tuples.
    """
    data = [
        {'Id': ('9e19b1558bbcba9202c1d3c4e26d8fe6e2c6060faad9a7074487e3b210a2'
                '6a16')},
        {'Id': ('b798acf4382421d231680d28aa62ae9b486b89711733c6acbb4cc85d8bec4'
                '072')},
    ]
    formatted = format_data('ps', data)
    print('\n')
    print('\n'.join(formatted))


def test_help_data_formatting():
    """
    Test formatting for list of tuples.
    """
    data = [
        ('help', "Help on available commands."),
        ('version', "Equivalent of 'docker version'."),
        ('ps', "Equivalent of 'docker ps'."),
        ('images', "Equivalent of 'docker images'."),
        ('run', "Equivalent of 'docker run'."),
        ('stop', "Equivalent of 'docker stop'."),
        ('info', "Equivalent of 'docker info'.")
    ]
    formatted = format_data('help', data)
    print('\n')
    print('\n'.join(formatted))


def test_rmi_data_formatting():
    """
    Test formatting for list of strings.
    """
    data = [
        "busybox:latest",
        "busybox:ubuntu-14.04",
        "busybox:buildroot-2014.02",
    ]
    formatted = format_data('rmi', data)
    print('\n')
    print('\n'.join(formatted))


def test_dict_data_formatting():
    """
    Test hierarchical data formatting
    """
    data = {
        'name': 'John',
        'profession': 'Developer',
        'hobbies': {
            'active': {
                'indoor': ['aikido', 'swimming'],
                'outdoor': ['hunting', 'fishing']
            },
            'passive': ['reading', 'painting']
        }
    }

    lines = format_struct(data, indent=2)

    print('\n')
    for line in lines:
        print(line)


def test_info_data_formatting():
    """
    Test complex structure formatting
    """
    data = {
        'Containers': 2,
        'Debug': 1,
        'DockerRootDir': '/mnt/sda1/var/lib/docker',
        'Driver': 'aufs',
        'DriverStatus': [
            ['Root Dir', '/mnt/sda1/var/lib/docker/aufs'],
            ['Backing Filesystem', 'extfs'],
            ['Dirs', '223'],
            ['Dirperm1 Supported', 'true']
        ],
        'ExecutionDriver': 'native-0.2',
        'ID': '37ZW:4G34:S24K:Z6S7:PUFE:FGW2:EVXG:NFHO:AZ62:EJU5:MPJ3:XPQZ',
        'IPv4Forwarding': 1,
        'Images': 219,
        'IndexServerAddress': 'https://index.docker.io/v1/',
        'InitPath': '/usr/local/bin/docker',
        'InitSha1': '9145575052383dbf64cede3bac278606472e027c',
        'KernelVersion': '3.18.11-tinycore64',
        'Labels': None,
        'MemTotal': 2105860096,
        'MemoryLimit': 1,
        'NCP': 4,
        'NEventsListener': 0,
        'NFd': 13,
        'NGoroutines': 19,
        'Name': 'boot2docker',
        'OperatingSystem': ('Boot2Docker 1.6.0 (TCL 5.4); master : a270c71 - '
                            'Thu Apr 16 19:50:36 UTC 2015'),
        'RegistryConfig': {
            'IndexConfigs': {
                'docker.io': {
                    'Mirrors': None,
                    'Name': 'docker.io',
                    'Official': True,
                    'Secure': True
                }
            },
            'InsecureRegistryCIDRs': ['127.0.0.0/8']
        },
        'SwapLimit': 1,
        'SystemTime': '2015-04-29T04:58:07.548655766Z'
    }

    lines = format_struct(data, indent=2)

    print('\n')
    for line in lines:
        print(line)
