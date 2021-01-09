import click
import logging
from typing import NoReturn
from dokerc.config.config import Config
from dokerc.client.estimate import (
    add_estimate_to_session,
    delete_estimate_from_session,
    get_estimate_from_session,
    get_estimates_from_session,
    list_distant_users_for_estimate,
    EstimateError,
)
from dokerc.utils.utils import update_token

logger = logging.getLogger("DOKERC")


def get_estimates(config: Config, token: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        estimates = get_estimates_from_session(
            server=config.server, token=config.session.token
        )
        if estimates:
            for estimate in estimates:
                click.echo(
                    "ID: {id}; User: {user}; Best-Case: {best_case}; Most-Likely-Case: {most_likely_case}; Worst-Case: {worst_case}".format(
                        id=estimate.id,
                        user=estimate.user,
                        best_case=estimate.best,
                        most_likely_case=estimate.most,
                        worst_case=estimate.worst,
                    )
                )
        else:
            logger.info("No estimates added to the session so far")
    except EstimateError as ee:
        logger.error(ee)


def get_estimate(config: Config, token: str, id: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        estimate = get_estimate_from_session(
            server=config.server, token=config.session.token, id=id
        )
        click.echo(
            "ID: {id}; Effort: {effort}; Standard-Deviation: {standard_deviation}".format(
                id=id,
                user=estimate.effort,
                standard_deviation=estimate.standard_deviation,
            )
        )
    except EstimateError as ee:
        logger.error(ee)


def list_distant_users(config: Config, token: str, id: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        list_distant_users_for_estimate(
            server=config.server, token=config.session.token, id=id
        )
    except EstimateError as ee:
        logger.error(ee)


def add_estimate(
    config: Config,
    token: str,
    id: str,
    user: str,
    best_case: float,
    most_likely_case: float,
    worst_case: float,
) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        add_estimate_to_session(
            server=config.server,
            token=config.session.token,
            id=id,
            user=user,
            best_case=best_case,
            most_likely_case=most_likely_case,
            worst_case=worst_case,
        )
        logger.info("Estimate added")
    except EstimateError as te:
        logger.error(te)


def delete_estimate(config: Config, token: str, id: str, user: str) -> NoReturn:
    if token:
        config = update_token(config=config, token=token)
    try:
        delete_estimate_from_session(
            server=config.server,
            token=config.session.token,
            id=id,
            user=user,
        )
        logger.info("Estimate removed")
    except EstimateError as te:
        logger.error(te)
