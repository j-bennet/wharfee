from __future__ import unicode_literals
from __future__ import print_function

from dockercli.formatter import format_data
from dockercli.formatter import format_struct


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
    formatted = format_data(data)
    print('\n')
    print('\n'.join(formatted))

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
        'OperatingSystem': 'Boot2Docker 1.6.0 (TCL 5.4); master : a270c71 - Thu Apr 16 19:50:36 UTC 2015',
        'RegistryConfig': {
            'IndexConfigs': {
                'docker.io': {
                    'Mirrors': None,
                    'Name': 'docker.io',
                    'Official': True,
                    'Secure': True
                }
            },
        'InsecureRegistryCIDRs': ['127.0.0.0/8']},
        'SwapLimit': 1,
        'SystemTime': '2015-04-29T04:58:07.548655766Z'
    }

    lines = format_struct(data, spaces=2)

    print('\n')
    for line in lines:
        print(line)
