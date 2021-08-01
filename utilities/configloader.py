import os

from yaml import load

try:
    from yaml import CLoader as YAMLLoader
except ImportError:
    from yaml import Loader as YAMLLoader


class ConfigLoader():
    def __init__(self, read_delimiter = "."):
        self._config = None
        self._delimiter = read_delimiter
        pass

    def load(self, file):
        if (not os.path.isfile(file)):
            raise FileNotFoundError(file)

        with open(file, "r") as config:
            self._config = load(config.read(), Loader=YAMLLoader)

        return self

    def get(self, key, default = None):
        try:
            if (type(self._config) == list):
                return self._get_config_item(key)

            if (type(self._config) == dict):
                return self._get_config_value(key)
        except Exception as e:
            print(str(e))
            return default

    def _get_config_item(self, index):
        if (not type(key) == int):
            raise TypeError("Config key MUST be an integer")

        return self._config[index]

    def _get_config_value(self, key):
        if (not type(key) == str):
            raise TypeError("Config key MUST be a string")
        try:
            return self._resolve_dict_value(self._config, key)
        except KeyError:
            raise KeyError(key + " not found!")

    def _resolve_dict_value(self, dictionary, key):
        if type(dictionary) is not dict:
            raise TypeError("Dict expected!")

        if (key.find(self._delimiter) == -1):
            if key not in dictionary:
                raise KeyError(key)

            return dictionary.get(key)

        position = key.find(self._delimiter)
        parent = key[:position]
        subkey = key[(position + 1):]

        return self._resolve_dict_value(dictionary.get(parent), subkey)

class ConfigException(Exception): ...