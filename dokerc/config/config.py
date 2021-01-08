from configparser import ConfigParser
from typing import NamedTuple
import os

DEFAULT_CONFIG_LOCATION = "~/.dokerc"
DEFAULT_CONFIG_NAME = "config.ini"

config_parser = ConfigParser()


class ConfigError(RuntimeError):
    pass


class Server(NamedTuple):
    address: str
    port: int
    endpoint: str


class User(NamedTuple):
    name: str


class Config(NamedTuple):
    server: Server
    user: User


def check_for_default_config():
    return os.path.exists(os.path.join(DEFAULT_CONFIG_LOCATION, DEFAULT_CONFIG_NAME))


def get_config(file=""):
    if file:
        if os.path.exists(file):
            config = config_parser.read(file)
        else:
            raise ConfigError("Unable to read provided config")
    else:
        if check_for_default_config():
            config = config_parser.read(
                os.path.join(DEFAULT_CONFIG_LOCATION, DEFAULT_CONFIG_NAME)
            )
        else:
            raise ConfigError("Unable to read default config")

    dok_config = Config(
        Server(
            config["SERVER"]["address"],
            config["SERVER"]["port"],
            config["SERVER"]["endpoint"],
        ),
        User(
            config["USER"]["name"],
        ),
    )

    return dok_config
