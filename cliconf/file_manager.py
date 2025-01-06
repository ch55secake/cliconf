import abc
from abc import ABCMeta
from typing import Tuple


class FileManager(metaclass=ABCMeta):
    """
    Formal implementation for each file manager type, currently supported are yaml and json
    """
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'read_file') and subclass.read_file and
                hasattr(subclass, 'write_file') and subclass.write_file and
                hasattr(subclass, 'get_full_path') or NotImplemented)

    @abc.abstractmethod
    def read_file(self, path: str) -> dict:
        """
        Read file from filesystem.
        :return: file content as a dictionary
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def write_file(self, content: dict, path: str) -> bool:
        """
        Write content to file at a given path.
        :param path: to write file to
        :param content: that will be written into file
        :return: bool based on write result
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_full_path(self, path: str) -> Tuple[str, bool]:
        """
        Get full path of file at given path.
        :param path: to get full path of
        :return: path as a string and if the directory already exists or not
        """
        raise NotImplementedError()