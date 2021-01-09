import json
import logging
import requests
from typing import NamedTuple, NoReturn
from dokerc.config.config import Server

logger = logging.getLogger("DOKERC")


class EstimateError(RuntimeError):
    pass


class Estimate(NamedTuple):
    id: str
    user: str
    best: float
    most: float
    worst: float


class DelphiEstimate(NamedTuple):
    effort: float
    standard_deviation: float


def get_estimates_from_session(server: Server, token: str) -> [Estimate]:
    url = "{address}:{port}{endpoint}/sessions/{token}/estimates".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            ests = values["estimates"]
            estimates = []
            if not ests:
                return estimates
            for est in ests:
                estimates.append(
                    Estimate(
                        est["WorkPackageID"],
                        est["UserName"],
                        est["BestCase"],
                        est["MostLikelyCase"],
                        est["WorstCase"],
                    )
                )
            return estimates
        else:
            raise EstimateError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")


def get_estimate_from_session(server: Server, token: str, id: str) -> DelphiEstimate:
    url = "{address}:{port}{endpoint}/sessions/{token}/estimates/{id}".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
        id=id,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            est = values["estimate"]
            dest = DelphiEstimate(est["Effort"], est["StandardDeviation"])
            message = values["message"]
            if message == "warning":
                logger.warning(values["hint"])
                users = values["users"]
                if users:
                    for user in users:
                        logger.warning("User: {user}".format(user=user))
            return dest
        else:
            raise EstimateError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")


def list_distant_users_for_estimate(server: Server, token: str, id: str) -> NoReturn:
    url = "{address}:{port}{endpoint}/sessions/{token}/estimates/{id}/users/distance".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
        id=id,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            users = values["users"]
            if users:
                for user in users:
                    logger.info("User: {user}".format(user=user))
        else:
            raise EstimateError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")


def add_estimate_to_session(
    server: Server,
    token: str,
    id: str,
    user: str,
    best_case: float,
    most_likely_case: float,
    worst_case: float,
) -> NoReturn:
    url = "{address}:{port}{endpoint}/sessions/{token}/estimates".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
    )
    try:
        res = requests.post(
            url,
            data={
                "id": id,
                "user": user,
                "b": best_case,
                "m": most_likely_case,
                "w": worst_case,
            },
        )
        if res.status_code != 200:
            values = res.json()
            raise EstimateError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")


def delete_estimate_from_session(
    server: Server, token: str, id: str, user: str
) -> NoReturn:
    url = "{address}:{port}{endpoint}/sessions/{token}/estimates/{user}/{id}".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
        user=user,
        id=id,
    )
    try:
        res = requests.delete(url)
        if res.status_code != 200:
            values = res.json()
            raise EstimateError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")
