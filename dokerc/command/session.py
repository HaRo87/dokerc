import click
import logging
import re
from typing import NoReturn
from dokerc.config.config import (
    Config,
    ConfigError,
    create_config,
    Server,
    Session,
    User,
)
from dokerc.client.session import (
    start_new_session,
    end_session,
    SessionError,
    join_existing_session,
    leave_existing_session,
)
from dokerc.utils.utils import update_token

logger = logging.getLogger("DOKERC")
token_re = re.compile(r"/sessions/([\d|\w]*)")


def start_session(config: Config, file: str) -> NoReturn:
    try:
        res = start_new_session(server=config.server)
        token = token_re.findall(res)[0]
        conf = update_token(config=config, token=token)
        try:
            create_config(config=conf, file=file, force=True)
        except ConfigError as ce:
            logger.error(ce)
        logger.info(
            "New session started - token for sharing: {token}".format(token=token)
        )
    except SessionError as se:
        logger.error(se)


def join_session(config: Config, file: str, name: str, token: str) -> NoReturn:
    user = config.user.name
    if name:
        user = name
    if token:
        config = update_token(config=config, token=token)
        try:
            create_config(config=config, file=file, force=True)
        except ConfigError as ce:
            logger.error(ce)
    try:
        join_existing_session(
            server=config.server, token=config.session.token, name=user
        )
        logger.info("You joined the session")
    except SessionError as se:
        logger.error(se)


def leave_session(config: Config, file: str, name: str, token: str) -> NoReturn:
    user = config.user.name
    if name:
        user = name
    if token:
        config = update_token(config=config, token=token)
        try:
            create_config(config=config, file=file, force=True)
        except ConfigError as ce:
            logger.error(ce)
    try:
        leave_existing_session(
            server=config.server, token=config.session.token, name=user
        )
        logger.info("You have left the session")
    except SessionError as se:
        logger.error(se)


def stop_session(config: Config, file: str) -> NoReturn:
    try:
        end_session(server=config.server, token=config.session.token)
        logger.info("Session stopped")
        conf = update_token(config=config, token="")
        try:
            create_config(config=conf, file=file, force=True)
        except ConfigError as ce:
            logger.error(ce)
    except SessionError as se:
        logger.error("Unable to stop session")
        logger.error(se)
