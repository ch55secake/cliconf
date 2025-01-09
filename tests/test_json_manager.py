import pytest
from unittest.mock import MagicMock, mock_open, patch
from json import JSONDecodeError
from cliconf.json_manager import JsonManager


@pytest.fixture
def json_manager():
    return JsonManager()


def test_write_file_success(mocker, json_manager):
    mock_get_full_path = mocker.patch.object(
        json_manager, "get_full_path", return_value=("/mocked/path/config.json", False)
    )
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open_file = mocker.patch("builtins.open", mock_open())

    assert json_manager.write_file({"key": "value"}, "/mocked/path") is True

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_makedirs.assert_called_once_with("/mocked/path", exist_ok=False)
    mock_open_file.assert_called_once_with("/mocked/path/config.json", "w")


def test_write_file_type_error(mocker, json_manager):
    mock_get_full_path = mocker.patch.object(
        json_manager, "get_full_path", return_value=("/mocked/path/config.json", False)
    )
    mock_makedirs = mocker.patch("os.makedirs")
    mock_open_file = mocker.patch("builtins.open", mock_open())
    mock_json_dump = mocker.patch("json.dump", side_effect=TypeError)

    assert json_manager.write_file({"invalid": set()}, "/mocked/path") is False

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_makedirs.assert_called_once_with("/mocked/path", exist_ok=False)
    mock_open_file.assert_called_once_with("/mocked/path/config.json", "w")
    mock_json_dump.assert_called_once()


def test_read_file_success(mocker, json_manager):
    mock_get_full_path = mocker.patch.object(
        json_manager, "get_full_path", return_value=("/mocked/path/config.json", True)
    )
    mock_open_file = mocker.patch("builtins.open", mock_open(read_data='{"key": "value"}'))
    mock_json_load = mocker.patch("json.load", return_value={"key": "value"})

    result = json_manager.read_file("/mocked/path")
    assert result == {"key": "value"}

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_open_file.assert_called_once_with("/mocked/path/config.json", "r")
    mock_json_load.assert_called_once()


def test_read_file_json_decode_error(mocker, json_manager):
    mock_get_full_path = mocker.patch.object(
        json_manager, "get_full_path", return_value=("/mocked/path/config.json", True)
    )
    mock_open_file = mocker.patch("builtins.open", mock_open(read_data="invalid json"))
    mock_json_load = mocker.patch("json.load", side_effect=JSONDecodeError("error", "", 0))

    result = json_manager.read_file("/mocked/path")
    assert result is None

    mock_get_full_path.assert_called_once_with("/mocked/path")
    mock_open_file.assert_called_once_with("/mocked/path/config.json", "r")
    mock_json_load.assert_called_once()


def test_get_full_path_exists(mocker, json_manager):
    mocker.patch("pathlib.Path.exists", return_value=True)

    full_path, path_exists = json_manager.get_full_path("/mocked/path")
    assert full_path == "/mocked/path/config.json"
    assert path_exists is True



def test_get_full_path_not_exists(mocker, json_manager):
    mocker.patch("pathlib.Path.exists", return_value=False)

    full_path, path_exists = json_manager.get_full_path("/mocked/path")
    assert full_path == "/mocked/path/config.json"
    assert path_exists is False
