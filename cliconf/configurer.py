import json
import os
from pathlib import Path
import yaml

class Configurer(object):

    def __init__(self, file_type: str, config: dict, path: str):
        """
        Create a configurer object. You need to provide file_type and the object that is intended to be persisted
        :param file_type: File type of the configuration
        :param config: expects the configuration object and will load it in matching the filetype
        :param path: Path to the configuration file
        """
        self.file_type = file_type
        self.config = config
        self.path = path

    def config_exists(self) -> bool:
        """
        Check if the configuration file exists and return that condition as a boolean
        :return: bool if the file exists or not
        """
        config_file_path = Path(f"{Path.home()}/{self.path}")
        if config_file_path.is_file():
            return True
        return False


    def safe_initialize(self) -> bool:
        """
        Check if the configuration file exists before attempting to initialize it
        :return:
        """
        if not self.config_exists():
            self.initialize()



    def initialize(self) -> bool:
        """
        Create configuration file, does not check if the configuration file exists before attempting to write.
        :return:
        """
        pass


    def read_configuration(self) -> object:
        """

        :return:
        """
        pass

    def write_json(self) -> bool:
        """
        Write a new json configuration file at the path on the configurer object.
        :return: boolean as a write result on whether the file was successfully created
        """
        full_path: str = os.path.join(self.path, "config.json")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as f:
            try :
                json.dump(self.config, f, sort_keys=True, indent=4,
                          ensure_ascii=False)
                return True
            except TypeError:
                return False

    def write_yaml(self) -> bool:
        """
        Write a new yaml configuration file at the path on the configurer object.
        :return: boolean as a write result on whether the file was successfully created or not
        """
        full_path: str = os.path.join(self.path, "config.yaml")
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w") as stream:
            try:
                yaml.dump(self.config, stream, default_flow_style=False)
                return True
            except yaml.YAMLError:
                return False
