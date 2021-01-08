import click
import logging
import os
from typing import NoReturn

from dokerc.config.config import (
    check_for_default_config,
    Config,
    Server,
    User,
    create_config,
    ConfigError,
)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(levelname)s [%(module)s] : %(message)s")
log_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.NOTSET, handlers=[log_handler])

logger = logging.getLogger("DOKERC")

config_option = click.option("--config", "-c", help="custom config file")


def global_options(o):
    o = config_option(o)
    return o


@click.group(chain=True)
def cli():
    pass


@cli.command()
def info():
    """Provides some general info about DokerC"""
    click.echo("DokerC a small CLI client for the Doker Backend.")
    click.echo("Checkout https://haro87.github.io/doker-meta for further info.")


@cli.command()
@click.option("--force", is_flag=True, help="forces to overwrite existing config file")
@global_options
def init(force, config):
    """Initialize DokerC - mainly generating the config"""
    if not force:
        if not config:
            if check_for_default_config():
                click.echo("Config file already present and no force flag provided.")
                click.confirm(
                    "Do you want to overwrite your default config?",
                    default="y",
                    abort=True,
                )
        else:
            if os.path.isfile(click.format_filename(config)):
                click.echo("Config file already present and no force flag provided.")
                click.confirm(
                    "Do you want to overwrite your config?",
                    default="y",
                    abort=True,
                )
        create_config_file(filename=config, force=force)


def create_config_file(filename: str, force: bool) -> NoReturn:
    """
    Creates the actual config file
    """
    server_address = click.prompt(
        "Enter the DokerB server address, please",
        default="http://localhost",
        type=str,
    )
    server_port = click.prompt(
        "Enter the DokerB server port, please", default=5000, type=int
    )
    server_endpoint = click.prompt(
        "Enter the DokerB API endpoint, please", default="/api", type=str
    )
    user_name = click.prompt("Enter your preferred user name, please", type=str)

    conf = Config(
        Server(
            server_address,
            server_port,
            server_endpoint,
        ),
        User(user_name),
    )
    try:
        create_config(config=conf, file=filename, force=force)
    except ConfigError as ce:
        logger.error(ce)
