from configparser import ConfigParser
import errno
import os
from pathlib import Path
from typing import NamedTuple, NoReturn


DEFAULT_CONFIG_LOCATION = ".dokerc"
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


class Session(NamedTuple):
    token: str


class Config(NamedTuple):
    server: Server
    user: User
    session: Session


def check_for_default_config() -> bool:
    return os.path.exists(
        os.path.join(Path.home(), DEFAULT_CONFIG_LOCATION, DEFAULT_CONFIG_NAME)
    )


def get_config(file="") -> Config:
    if file:
        if os.path.exists(file):
            config_parser.read(file)
        else:
            raise ConfigError("Unable to read provided config")
    else:
        if check_for_default_config():
            config_parser.read(
                os.path.join(Path.home(), DEFAULT_CONFIG_LOCATION, DEFAULT_CONFIG_NAME)
            )
        else:
            raise ConfigError("Unable to read default config")

    server = config_parser["SERVER"]
    user = config_parser["USER"]
    session = config_parser["SESSION"]

    dok_config = Config(
        Server(
            server["address"],
            server["port"],
            server["endpoint"],
        ),
        User(
            user["name"],
        ),
        Session(
            session["token"],
        ),
    )

    return dok_config


def validate_config(config: Config) -> NoReturn:
    if not config.server.address:
        raise ConfigError("Invalid server address")
    if config.server.port < 0:
        raise ConfigError("Invalid server port")
    if not config.user.name:
        raise ConfigError("Invalid user name")


def create_config(config: Config, file="", force=False) -> NoReturn:
    validate_config(config=config)
    if not file:
        file = os.path.join(Path.home(), DEFAULT_CONFIG_LOCATION, DEFAULT_CONFIG_NAME)
    if os.path.exists(file):
        if force:
            _write_config(config=config, file=file)
        else:
            raise ConfigError("Config file exists and no force arg provided")
    else:
        _write_config(config=config, file=file)


def _write_config(config: Config, file: str) -> NoReturn:
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except OSError as err:
            if err.errno != errno.EEXIST:
                raise

    config_parser["SERVER"] = {
        "address": config.server.address,
        "port": config.server.port,
        "endpoint": config.server.endpoint,
    }
    config_parser["USER"] = {"name": config.user.name}
    config_parser["SESSION"] = {"token": config.session.token}
    with open(file, "w") as conf:
        config_parser.write(conf)
