import click
import logging
import os
import re
from typing import NoReturn

from dokerc.config.config import (
    check_for_default_config,
    Config,
    Server,
    User,
    Session,
    create_config,
    ConfigError,
    get_config,
)

from dokerc.client.session import start_new_session, SessionError, end_session

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(levelname)s [%(module)s] : %(message)s")
log_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.NOTSET, handlers=[log_handler])

logger = logging.getLogger("DOKERC")

config_option = click.option("--config", "-c", help="custom config file")

token_re = re.compile(r"/sessions/([\d|\w]*)")


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
                force = True
        else:
            if os.path.isfile(click.format_filename(config)):
                click.echo("Config file already present and no force flag provided.")
                click.confirm(
                    "Do you want to overwrite your config?",
                    default="y",
                    abort=True,
                )
                force = True
        create_config_file(filename=config, force=force)


@cli.command()
@global_options
def start_session(config):
    try:
        conf = get_config(config)
    except ConfigError as ce:
        logger.error(ce)
    try:
        res = start_new_session(server=conf.server)
        token = token_re.findall(res)[0]
        conf = update_token(config=conf, token=token)
        try:
            create_config(config=conf, file=config, force=True)
        except ConfigError as ce:
            logger.error(ce)
        logger.info("New session started")
    except SessionError as se:
        logger.error(se)


@cli.command()
@global_options
def stop_session(config):
    try:
        conf = get_config(config)
    except ConfigError as ce:
        logger.error(ce)
    try:
        res = end_session(server=conf.server, token=conf.session.token)
        if res:
            logger.info("Session stopped")
            conf = update_token(config=conf, token="")
            try:
                create_config(config=conf, file=config, force=True)
            except ConfigError as ce:
                logger.error(ce)
        else:
            logger.error("Unable to stop session")
    except SessionError as se:
        logger.error(se)


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
        Session(""),
    )
    try:
        create_config(config=conf, file=filename, force=force)
    except ConfigError as ce:
        logger.error(ce)


def update_token(config: Config, token: str) -> Config:
    conf = Config(
        Server(
            config.server.address,
            int(config.server.port),
            config.server.endpoint,
        ),
        User(config.user.name),
        Session(token),
    )
    return conf