import os
from pathlib import Path
from typing import Tuple

import yaml

from cliconf.file_manager import FileManager


class YamlManager(FileManager):
    """
    Read and write yaml files to/from the path provided
    """
    def write_file(self, content: dict, path: str) -> bool:
        """
        :param content: that you want to write to the yaml file
        :param path: where to write the yaml file
        :return: bool based on the write result
        """
        full_path, path_existence = self.get_full_path(path)
        if not path_existence:
            os.makedirs(os.path.dirname(full_path), exist_ok=False)
        with open(full_path, "w") as stream:
            try:
                yaml.dump(content, stream, default_flow_style=False)
                return True
            except yaml.YAMLError:
                return False

    def read_file(self, path: str) -> dict | None:
        """
        :param path: to read the yaml file from
        :return: the contents of the yaml file unless it errors then it will return None
        """
        full_path, _path_existence = self.get_full_path(path)
        with open(full_path, "r") as stream:
            try:
                return yaml.safe_load(stream)
            except yaml.YAMLError:
                return None

    def get_full_path(self, path: str) -> Tuple[str, bool]:
        """
        :param path: to get
        :return: tuple of full path and whether it exists or not
        """
        full_path: str = os.path.join(path, "config.yaml")
        return full_path, Path.exists(Path(full_path))