import json
import requests
from dokerc.config.config import Server
from dokerc.utils.utils import get_base_url


class UserError(RuntimeError):
    pass


def get_users_from_session(server: Server, token: str) -> [str]:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/users".format(
        base=base,
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