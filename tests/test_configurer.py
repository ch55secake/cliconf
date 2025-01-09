import pytest

from cliconf.configurer import Configurer


@pytest.fixture
def configurer_json():
    return Configurer(file_type="json", config={"key": "value"}, path=None, app_name="test_app")


@pytest.fixture
def configurer_yaml():
    return Configurer(file_type="yaml", config={"key": "value"}, path=None, app_name="test_app")


def test_initializer_defaults_path(configurer_json):
    assert configurer_json.path == "$HOME/.config/test_app/config.yml"


def test_config_exists(mocker, configurer_json):
    mock_path = mocker.patch("pathlib.Path.exists", return_value=True)
    assert configurer_json.config_exists() is True
    mock_path.assert_called_once()


def test_config_does_not_exist(mocker, configurer_json):
    mock_path = mocker.patch("pathlib.Path.exists", return_value=False)
    assert configurer_json.config_exists() is False
    mock_path.assert_called_once()


def test_initialize_with_yaml(mocker, configurer_yaml):
    mock_yaml_manager = mocker.patch("cliconf.yaml_manager.YamlManager.write_file", return_value=True)
    assert configurer_yaml.initialize() is True
    mock_yaml_manager.assert_called_once_with(content={"key": "value"}, path="$HOME/.config/test_app/config.yml")


def test_initialize_with_json(mocker, configurer_json):
    mock_json_manager = mocker.patch("cliconf.json_manager.JsonManager.write_file", return_value=True)
    assert configurer_json.initialize() is True
    mock_json_manager.assert_called_once_with(content={"key": "value"}, path="$HOME/.config/test_app/config.yml")


def test_safe_initialize_file_exists(mocker, configurer_json):
    mock_exists = mocker.patch.object(configurer_json, "config_exists", return_value=True)
    assert configurer_json.safe_initialize() is None
    mock_exists.assert_called_once()


def test_safe_initialize_file_does_not_exist(mocker, configurer_json):
    mock_exists = mocker.patch.object(configurer_json, "config_exists", return_value=False)
    mock_initialize = mocker.patch.object(configurer_json, "initialize", return_value=True)
    assert configurer_json.safe_initialize() is True
    mock_exists.assert_called_once()
    mock_initialize.assert_called_once()


def test_read_configuration_with_yaml(mocker, configurer_yaml):
    mock_yaml_manager = mocker.patch("cliconf.yaml_manager.YamlManager.read_file", return_value={"key": "value"})
    result = configurer_yaml.read_configuration()
    assert result == {"key": "value"}
    mock_yaml_manager.assert_called_once_with(path="$HOME/.config/test_app/config.yml")


def test_read_configuration_with_json(mocker, configurer_json):
    mock_json_manager = mocker.patch("cliconf.json_manager.JsonManager.read_file", return_value={"key": "value"})
    result = configurer_json.read_configuration()
    assert result == {"key": "value"}
    mock_json_manager.assert_called_once_with(path="$HOME/.config/test_app/config.yml")
