import json
import requests
from typing import NamedTuple
from dokerc.config.config import Server


class SessionError(RuntimeError):
    pass


def start_new_session(server: Server) -> str:
    url = "{address}:{port}{endpoint}/sessions".format(
        address=server.address, port=server.port, endpoint=server.endpoint
    )
    res = requests.post(url)
    values = res.json()
    if res.status_code == 200:
        route = values["route"]
        return route
    else:
        raise SessionError(values["reason"])


def end_session(server: Server, token: str) -> bool:
    url = "{address}:{port}{endpoint}/sessions/{token}".format(
        address=server.address, port=server.port, endpoint=server.endpoint, token=token
    )
    res = requests.delete(url)
    if res.status_code == 200:
        return True
    else:
        return False
