import click
import logging
from typing import NoReturn
from dokerc.config.config import Config
from dokerc.client.user import get_users_from_session, UserError
from dokerc.utils.utils import update_token

logger = logging.getLogger("DOKERC")


def get_users(config: Config, token: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        users = get_users_from_session(server=config.server, token=config.session.token)
        if users:
            for user in users:
                click.echo(user)
        else:
            logger.info("No users joined the session so far")
    except UserError as ue:
        logger.error(ue)