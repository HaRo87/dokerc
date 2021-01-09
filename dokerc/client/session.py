import json
import requests
from dokerc.config.config import Server


class SessionError(RuntimeError):
    pass


def start_new_session(server: Server) -> str:
    url = "{address}:{port}{endpoint}/sessions".format(
        address=server.address, port=server.port, endpoint=server.endpoint
    )
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


def join_existing_session(server: Server, token: str, name: str) -> bool:
    url = "{address}:{port}{endpoint}/sessions/{token}/users".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
    )
    try:
        res = requests.post(url, data={"name": name})
        if res.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


def leave_existing_session(server: Server, token: str, name: str) -> bool:
    url = "{address}:{port}{endpoint}/sessions/{token}/users/{user}".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
        user=name,
    )
    try:
        res = requests.delete(url)
        if res.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False


def end_session(server: Server, token: str) -> bool:
    url = "{address}:{port}{endpoint}/sessions/{token}".format(
        address=server.address, port=server.port, endpoint=server.endpoint, token=token
    )
    try:
        res = requests.delete(url)
        if res.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.ConnectionError:
        return False