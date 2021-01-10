import json
import logging
import requests
from typing import NamedTuple, NoReturn
from dokerc.config.config import Server
from dokerc.utils.utils import get_base_url

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
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/estimates".format(
        base=base,
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
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/estimates/{id}".format(
        base=base,
        token=token,
        id=id,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            est = values["estimate"]
            dest = DelphiEstimate(est["effort"], est["standarddeviation"])
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
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/estimates/{id}/users/distance".format(
        base=base,
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
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/estimates".format(
        base=base,
        token=token,
    )
    try:
        payload = {
            "b": best_case,
            "id": id,
            "m": most_likely_case,
            "user": user,
            "w": worst_case,
        }
        res = requests.post(
            url,
            json=payload,
        )
        if res.status_code != 200:
            values = res.json()
            raise EstimateError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise EstimateError("Unable to reach backend")


def delete_estimate_from_session(
    server: Server, token: str, id: str, user: str
) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/estimates/{user}/{id}".format(
        base=base,
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
