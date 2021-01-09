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

from dokerc.command.session import (
    start_session,
    stop_session,
    join_session,
    leave_session,
)

from dokerc.command.user import get_users

from dokerc.command.task import (
    add_task,
    clear_estimate,
    delete_task,
    get_tasks,
    update_task,
)

from dokerc.command.estimate import (
    add_estimate,
    delete_estimate,
    get_estimate,
    get_estimates,
    list_distant_users,
)

log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)
log_formatter = logging.Formatter("%(levelname)s [%(module)s] : %(message)s")
log_handler.setFormatter(log_formatter)

logging.basicConfig(level=logging.NOTSET, handlers=[log_handler])

logger = logging.getLogger("DOKERC")

config_option = click.option("--config", "-c", help="custom config file")
token_option = click.option("--token", "-t", help="custom session token")
user_option = click.option("--user", "-u", help="custom user name")
id_argument = click.argument("id", required=True)


def global_options(o):
    o = config_option(o)
    return o


def sub_global_option(s):
    s = user_option(s)
    s = token_option(s)
    return s


def sub_global_args(a):
    a = id_argument(a)
    return a


@click.group()
def cli():
    """DokerC CLI client for the Delphi Planning Poker Backend"""
    pass


@cli.group()
def session():
    """All commands related to session handling"""
    pass


@cli.group()
def users():
    """All commands related to users"""
    pass


@cli.group()
def tasks():
    """All commands related to tasks"""
    pass


@cli.group()
def estimates():
    """All commands related to estimates"""
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


@session.command()
@global_options
def start(config):
    """Starts a new Doker session"""
    try:
        conf = get_config(config)
        start_session(config=conf, file=config)
    except ConfigError as ce:
        logger.error(ce)


@session.command()
@global_options
def stop(config):
    """Stops the current Doker session - all data will be deleted"""
    try:
        conf = get_config(config)
        stop_session(config=conf, file=config)
    except ConfigError as ce:
        logger.error(ce)


@session.command()
@global_options
@sub_global_option
def join(config, user, token):
    """Adds you to the current active Doker session"""
    try:
        conf = get_config(config)
        join_session(config=conf, file=config, name=user, token=token)
    except ConfigError as ce:
        logger.error(ce)


@session.command()
@global_options
@sub_global_option
def leave(config, user, token):
    """Removes you from the current active Doker session"""
    try:
        conf = get_config(config)
        leave_session(config=conf, file=config, name=user, token=token)
    except ConfigError as ce:
        logger.error(ce)


@users.command()
@global_options
@sub_global_option
def list(config, user, token):
    """Lists all user who are part of the session"""
    try:
        conf = get_config(config)
        get_users(config=conf, token=token)
    except ConfigError as ce:
        logger.error(ce)


@tasks.command()
@global_options
@sub_global_option
def get(config, user, token):
    """Gets all tasks which are part of the session"""
    try:
        conf = get_config(config)
        get_tasks(config=conf, token=token)
    except ConfigError as ce:
        logger.error(ce)


@tasks.command()
@global_options
@sub_global_option
@sub_global_args
@click.option("--summary", help="short summary")
def add(config, user, token, id, summary):
    """Adds a new task to the session"""
    try:
        conf = get_config(config)
        add_task(config=conf, token=token, id=id, summary=summary)
    except ConfigError as ce:
        logger.error(ce)


@tasks.command()
@global_options
@sub_global_option
@sub_global_args
@click.option("--effort", required=True, type=float, help="effort")
@click.option("--std", required=True, type=float, help="standard deviation")
def update(config, user, token, id, effort, std):
    """Adds a new task to the session"""
    try:
        conf = get_config(config)
        update_task(
            config=conf,
            token=token,
            id=id,
            effort=effort,
            standard_deviation=std,
        )
    except ConfigError as ce:
        logger.error(ce)


@tasks.command()
@global_options
@sub_global_option
@sub_global_args
def remove(config, user, token, id):
    """Removes a task from the session"""
    try:
        conf = get_config(config)
        delete_task(
            config=conf,
            token=token,
            id=id,
        )
    except ConfigError as ce:
        logger.error(ce)


@tasks.command()
@global_options
@sub_global_option
@sub_global_args
def clear(config, user, token, id):
    """Clears the estimate of a task"""
    try:
        conf = get_config(config)
        clear_estimate(
            config=conf,
            token=token,
            id=id,
        )
    except ConfigError as ce:
        logger.error(ce)


@estimates.command()
@global_options
@sub_global_option
@sub_global_args
@click.option("--best", required=True, type=float, help="best case")
@click.option("--most", required=True, type=float, help="most likely case")
@click.option("--worst", required=True, type=float, help="worst case")
def submit(config, user, token, id, best, most, worst):
    """Submits a new estimate to the session"""
    try:
        conf = get_config(config)
        add_estimate(
            config=conf,
            token=token,
            id=id,
            user=user,
            best_case=best,
            most_likely_case=most,
            worst_case=worst,
        )
    except ConfigError as ce:
        logger.error(ce)


@estimates.command()
@global_options
@sub_global_option
def all(config, user, token):
    """Shows all estimates which are part of the session"""
    try:
        conf = get_config(config)
        get_estimates(config=conf, token=token)
    except ConfigError as ce:
        logger.error(ce)


@estimates.command()
@global_options
@sub_global_option
@sub_global_args
def calc(config, user, token, id):
    """Shows the calculated delphi estimate for the specified task"""
    try:
        conf = get_config(config)
        get_estimate(config=conf, token=token, id=id)
    except ConfigError as ce:
        logger.error(ce)


@estimates.command()
@global_options
@sub_global_option
@sub_global_args
def distant(config, user, token, id):
    """Shows the users who had the biggest distance between their estimates"""
    try:
        conf = get_config(config)
        list_distant_users(config=conf, token=token, id=id)
    except ConfigError as ce:
        logger.error(ce)


@estimates.command()
@global_options
@sub_global_option
@sub_global_args
def delete(config, user, token, id):
    """Deletes the estimate of a specified user for a specified task"""
    try:
        conf = get_config(config)
        delete_estimate(config=conf, token=token, id=id, user=user)
    except ConfigError as ce:
        logger.error(ce)


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
