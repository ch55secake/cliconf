from enum import Enum


class FileType(Enum):
    """
    Supported file types for writing config to.
    """
    JSON = 'json'
    YAML = 'yaml'