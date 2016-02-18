# -*- coding: utf-8
from __future__ import unicode_literals

import pytest
from mock import Mock, patch
from docker.errors import InvalidVersion
from docker.api.volume import VolumeApiMixin
from wharfee.client import DockerClient


@pytest.fixture
def client():
    clear = Mock()
    refresh = Mock()
    return DockerClient(clear_handler=clear, refresh_handler=refresh)


@patch.object(VolumeApiMixin, 'volumes', side_effect=InvalidVersion('Not supported.'))
def test_invalid_version(mock_volumes, client):
    result = client.volume_ls()
    assert mock_volumes.called
    assert result is None

