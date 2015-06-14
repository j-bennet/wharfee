from __future__ import unicode_literals

import pytest
from dockercli.client import DockerClient


@pytest.fixture
def client():
    return DockerClient(clear_handler=lambda: None)


@pytest.mark.parametrize("client, ports, expected", [
    (client(), ['3306'], {'3306': None}),
    (client(), ['9999:3306'], {'3306': '9999'}),
    (client(), ['0.0.0.0:9999:3306'], {'3306': ('0.0.0.0', '9999')}),
    (client(),
     ['9999:3306', '127.0.0.1::8001'],
     {'8001': ('127.0.0.1', None), '3306': '9999'}),
])
def test_port_parsing(client, ports, expected):
    """
    Parse port mappings.
    """
    result = client.parse_port_bindings(ports)

    assert result == expected
