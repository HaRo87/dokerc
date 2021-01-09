import click
import logging
from typing import NoReturn
from dokerc.config.config import Config
from dokerc.client.task import (
    add_task_to_session,
    clear_estimate_of_task,
    delete_task_from_session,
    get_tasks_from_session,
    update_task_of_session,
    TaskError,
)
from dokerc.utils.utils import update_token

logger = logging.getLogger("DOKERC")


def get_tasks(config: Config, token: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        tasks = get_tasks_from_session(server=config.server, token=config.session.token)
        if tasks:
            for task in tasks:
                click.echo(
                    "ID: {id}; Summary: {summary}; Effort: {effort}; Standard Deviation: {standard_deviation}".format(
                        id=task.id,
                        summary=task.summary,
                        effort=task.effort,
                        standard_deviation=task.standard_deviation,
                    )
                )
        else:
            logger.info("No tasks added to the session so far")
    except TaskError as te:
        logger.error(te)


def add_task(config: Config, token: str, id: str, summary: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        add_task_to_session(
            server=config.server, token=config.session.token, id=id, summary=summary
        )
        logger.info("Task added")
    except TaskError as te:
        logger.error(te)


def update_task(
    config: Config, token: str, id: str, effort: float, standard_deviation: float
) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        update_task_of_session(
            server=config.server,
            token=config.session.token,
            id=id,
            effort=effort,
            standard_deviation=standard_deviation,
        )
        logger.info("Task updated")
    except TaskError as te:
        logger.error(te)


def delete_task(config: Config, token: str, id: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        delete_task_from_session(
            server=config.server,
            token=config.session.token,
            id=id,
        )
        logger.info("Task removed")
    except TaskError as te:
        logger.error(te)


def clear_estimate(config: Config, token: str, id: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        clear_estimate_of_task(
            server=config.server,
            token=config.session.token,
            id=id,
        )
        logger.info("Cleared estimate of task")
    except TaskError as te:
        logger.error(te)