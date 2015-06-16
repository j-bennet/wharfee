from __future__ import unicode_literals

import pytest
from dockercli.helpers import parse_port_bindings


@pytest.mark.parametrize("ports, expected", [
    (['3306'], {'3306': None}),
    (['9999:3306'], {'3306': '9999'}),
    (['0.0.0.0:9999:3306'], {'3306': ('0.0.0.0', '9999')}),
    (['9999:3306', '127.0.0.1::8001'],
     {'8001': ('127.0.0.1', None), '3306': '9999'}),
])
def test_port_parsing(ports, expected):
    """
    Parse port mappings.
    """
    result = parse_port_bindings(ports)

    assert result == expected
