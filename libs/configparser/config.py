# coding=utf-8
import json
from os.path import isfile

import yaml

from classes import Exceptions


class ConfigParser:
    """
    ConfigParser for YAML and JSON
    Supports context managers: loads config automatically when entering the with block, and does nothing when exiting
    Supports being looped over in a for statement: yields items in self.config
    :param config_location: Absolute path to the config file
    :param _type: type of config file: 1 for YAML, 2 for JSON
    :raises Exceptions.NotAFileError: if config_location is not a file
    :raises Exceptions.UnsupportedConfigType: if _type is not between 1 and 2
    """

    def __init__(self, config_location, _type: int = 1):
        if not isfile(config_location):
            raise Exceptions.NotAFileError
        if not 0 < _type < 2:
            raise Exceptions.UnsupportedConfigType
        self.config_location = config_location
        self.config = None
        self.type = _type

    def __iter__(self):
        for i in self.config:
            yield i

    def __enter__(self):
        self.load_config()
        return self

    def __exit__(self):
        pass

    def load_config(self):
        """
        Loads config that was defined when created
        :return: Config
        :raises Exceptions.FormattingError: if a exceptions is created by the loaders
        """
        if self.type == 1:
            with open(self.config_location, "r") as cf:
                try:
                    self.config = yaml.safe_load(
                        cf)  # Use safe_load instead of load to keep arbitrary Python code from being executed
                except yaml.YAMLError as e:
                    raise Exceptions.FormattingError(e)
        elif self.type == 2:
            with open(self.config_location, "r") as cf:
                try:
                    self.config = json.loads(cf.read())
                except json.JSONDecodeError as e:
                    raise Exceptions.FormattingError(e)
        else:
            raise Exceptions.UnsupportedConfigType
        return self.config

    def reload_config(self):
        """
        Loads config: alias for load_config() but returns nothing
        """
        self.load_config()

    def get_config(self):
        """
        :return: Config
        """
        return self.config
