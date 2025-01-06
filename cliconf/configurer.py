from pathlib import Path

from cliconf.file_type import FileType
from cliconf.json_manager import JsonManager
from cliconf.yaml_manager import YamlManager


class Configurer(object):

    def __init__(self, file_type: str, config: dict, path: str | None, app_name: str):
        """
        Create a configurer object. You need to provide file_type and the object that is intended to be persisted
        :param file_type: File type of the configuration
        :param config: expects the configuration object and will load it in matching the filetype
        :param path: Path to the configuration file
        :param app_name: Name of the application, used for defaulting the path and filetype to yaml
        """
        self.file_type = FileType(file_type)
        self.config = config
        self.path = path
        if path is None:
            self.path = f"$HOME/.config/{app_name}.yml"
        self.app_name = app_name


    def config_exists(self) -> bool:
        """
        Check if the configuration file exists and return that condition as a boolean
        :return: bool if the file exists or not
        """
        config_file_path = Path(f"{Path.home()}/{self.path}")
        return config_file_path.exists()


    def safe_initialize(self) -> bool:
        """
        Check if the configuration file exists before attempting to initialize it
        :return: returns true if the configuration file exists and has been initialized
        """
        if not self.config_exists():
            return self.initialize()




    def initialize(self) -> bool:
        """
        Create configuration file, does not check if the configuration file exists before attempting to write.
        :return:
        """
        match self.file_type:
            case FileType.YAML:
                yaml_manager: YamlManager = YamlManager()
                return yaml_manager.write_file(content=self.config, path=self.path)
            case FileType.JSON:
                json_manager: JsonManager = JsonManager()
                return json_manager.write_file(content=self.config, path=self.path)


    def read_configuration(self) -> dict:
        """
        Reads the configuration file from the default path
        :return:
        """
        match self.file_type:
            case FileType.YAML:
                yaml_manager: YamlManager = YamlManager()
                return yaml_manager.read_file(path=self.path)
            case FileType.JSON:
                json_manager: JsonManager = JsonManager()
                return json_manager.read_file(path=self.path)