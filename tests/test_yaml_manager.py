import pytest
from unittest.mock import mock_open, patch
from cliconf.yaml_manager import YamlManager
import yaml


@pytest.fixture
def yaml_manager():
    return YamlManager()


def test_write_file_success(mocker, yaml_manager):
    mock_get_full_path = mocker.patch.object(
        yaml_manager, "get_full_path", return_value=("/mocked/path/config.yaml", False)
    )
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open_file = mocker.patch("builtins.open", mock_open())
    mock_yaml_dump = mocker.patch("yaml.dump")

    result = yaml_manager.write_file({"key": "value"}, "/mocked/path")
    assert result is True

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_makedirs.assert_called_once_with("/mocked/path", exist_ok=False)
    mock_open_file.assert_called_once_with("/mocked/path/config.yaml", "w")
    mock_yaml_dump.assert_called_once_with({"key": "value"}, mock_open_file(), default_flow_style=False)


def test_write_file_yaml_error(mocker, yaml_manager):
    mock_get_full_path = mocker.patch.object(
        yaml_manager, "get_full_path", return_value=("/mocked/path/config.yaml", False)
    )
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open_file = mocker.patch("builtins.open", mock_open())
    mock_yaml_dump = mocker.patch("yaml.dump", side_effect=yaml.YAMLError)

    result = yaml_manager.write_file({"key": "value"}, "/mocked/path")
    assert result is False

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_makedirs.assert_called_once_with("/mocked/path", exist_ok=False)
    mock_open_file.assert_called_once_with("/mocked/path/config.yaml", "w")
    mock_yaml_dump.assert_called_once()


def test_read_file_success(mocker, yaml_manager):
    mock_get_full_path = mocker.patch.object(
        yaml_manager, "get_full_path", return_value=("/mocked/path/config.yaml", True)
    )
    mock_open_file = mocker.patch("builtins.open", mock_open(read_data="key: value"))
    mock_yaml_safe_load = mocker.patch("yaml.safe_load", return_value={"key": "value"})

    result = yaml_manager.read_file("/mocked/path")
    assert result == {"key": "value"}

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_open_file.assert_called_once_with("/mocked/path/config.yaml", "r")
    mock_yaml_safe_load.assert_called_once_with(mock_open_file())


def test_read_file_yaml_error(mocker, yaml_manager):
    mock_get_full_path = mocker.patch.object(
        yaml_manager, "get_full_path", return_value=("/mocked/path/config.yaml", True)
    )
    mock_open_file = mocker.patch("builtins.open", mock_open(read_data="invalid: yaml"))
    mock_yaml_safe_load = mocker.patch("yaml.safe_load", side_effect=yaml.YAMLError)

    result = yaml_manager.read_file("/mocked/path")
    assert result is None

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_open_file.assert_called_once_with("/mocked/path/config.yaml", "r")
    mock_yaml_safe_load.assert_called_once()


def test_get_full_path_exists(mocker, yaml_manager):
    mocker.patch("pathlib.Path.exists", return_value=True)

    full_path, path_exists = yaml_manager.get_full_path("/mocked/path")
    assert full_path == "/mocked/path/config.yaml"
    assert path_exists is True


def test_get_full_path_not_exists(mocker, yaml_manager):
    mocker.patch("pathlib.Path.exists", return_value=False)

    full_path, path_exists = yaml_manager.get_full_path("/mocked/path")
    assert full_path == "/mocked/path/config.yaml"
    assert path_exists is False

