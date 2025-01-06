import json
import os
from json import JSONDecodeError
from pathlib import Path
from typing import Tuple

from cliconf.file_manager import FileManager


class JsonManager(FileManager):
    """
    Read and write JSON files to/from the path provided
    """
    def write_file(self, content: dict, path: str) -> bool:
        """
        :param content: to write into the file
        :param path:
        :return:
        """
        full_path, path_existence = self.get_full_path(path)
        if not path_existence:
            os.makedirs(os.path.dirname(full_path), exist_ok=False)
        with open(full_path, "w") as f:
            try:
                json.dump(path, f, sort_keys=True, indent=4,
                          ensure_ascii=False)
                return True
            except TypeError:
                return False

    def read_file(self, path: str) -> dict | None:
        """
        :param path: to read json data into dict from
        :return: json data from file as dict, will return None if the load operation fails
        """
        full_path, _path_existence = self.get_full_path(path)
        with open(full_path, "r") as stream:
            try:
                return json.load(stream)
            except JSONDecodeError:
                return None


    def get_full_path(self, path: str) -> Tuple[str, bool]:
        """
        :param path: to get
        :return: tuple of full path and whether it exists or not
        """
        full_path: str = os.path.join(path, "config.json")
        return full_path, Path.exists(Path(full_path))