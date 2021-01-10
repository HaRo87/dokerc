import json
import requests
from typing import NoReturn
from dokerc.config.config import Server
from dokerc.utils.utils import get_base_url


class SessionError(RuntimeError):
    pass


def start_new_session(server: Server) -> str:
    base = get_base_url(server=server)
    url = "{base}/sessions".format(base=base)
    try:
        res = requests.post(url)
        values = res.json()
        if res.status_code == 200:
            route = values["route"]
            return route
        else:
            raise SessionError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise SessionError("Unable to reach backend")


def join_existing_session(server: Server, token: str, name: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/users".format(
        base=base,
        token=token,
    )
    try:
        payload = {"name": name}
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            values = res.json()
            raise SessionError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise SessionError("Unable to reach backend")


def leave_existing_session(server: Server, token: str, name: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/users/{user}".format(
        base=base,
        token=token,
        user=name,
    )
    try:
        res = requests.delete(url)
        if res.status_code != 200:
            values = res.json()
            raise SessionError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise SessionError("Unable to reach backend")


def end_session(server: Server, token: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}".format(base=base, token=token)
    try:
        res = requests.delete(url)
        if res.status_code != 200:
            values = res.json()
            raise SessionError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise SessionError("Unable to reach backend")