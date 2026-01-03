# -*- coding: utf-8
import sys
import pytest

from mock import Mock, patch, MagicMock
from docker.errors import InvalidVersion
from docker.api.volume import VolumeApiMixin
from wharfee.client import DockerClient


@pytest.fixture
def client():
    clear = Mock()
    refresh = Mock()
    # Mock the Docker API client to avoid needing a real Docker connection
    with patch('wharfee.client.DockerAPIClient') as mock_api:
        mock_api.return_value = MagicMock()
        return DockerClient(clear_handler=clear, refresh_handler=refresh)


@pytest.mark.skipif(sys.platform.startswith('win32'), reason="Not running on windows.")
@patch.object(VolumeApiMixin, 'volumes', side_effect=InvalidVersion('Not supported.'))
def test_invalid_version(mock_volumes):
    clear = Mock()
    refresh = Mock()
    with patch('wharfee.client.DockerAPIClient') as mock_api:
        mock_instance = MagicMock()
        mock_api.return_value = mock_instance
        mock_instance.volumes = Mock(side_effect=InvalidVersion('Not supported.'))
        client = DockerClient(clear_handler=clear, refresh_handler=refresh)
        result = client.volume_ls()
        assert mock_instance.volumes.called
        assert result is None

