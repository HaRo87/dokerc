import json
import requests
from dokerc.config.config import Server


class UserError(RuntimeError):
    pass


def get_users_from_session(server: Server, token: str) -> [str]:
    url = "{address}:{port}{endpoint}/sessions/{token}/users".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            users = values["users"]
            return users
        else:
            raise UserError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise UserError("Unable to reach backend")