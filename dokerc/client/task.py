import json
import requests
from typing import NamedTuple, NoReturn
from dokerc.config.config import Server
from dokerc.utils.utils import get_base_url


class TaskError(RuntimeError):
    pass


class Task(NamedTuple):
    id: str
    summary: str
    effort: float
    standard_deviation: float


def get_tasks_from_session(server: Server, token: str) -> [Task]:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/workpackages".format(
        base=base,
        token=token,
    )
    try:
        res = requests.get(url)
        values = res.json()
        if res.status_code == 200:
            wps = values["workpackages"]
            tasks = []
            if not wps:
                return tasks
            for wp in wps:
                tasks.append(
                    Task(
                        wp["ID"],
                        wp["Summary"],
                        wp["Effort"],
                        wp["StandardDeviation"],
                    )
                )
            return tasks
        else:
            raise TaskError(values["reason"])
    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")


def add_task_to_session(server: Server, token: str, id: str, summary: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/workpackages".format(
        base=base,
        token=token,
    )
    try:
        payload = {"id": id, "summary": summary}
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")


def update_task_of_session(
    server: Server, token: str, id: str, effort: float, standard_deviation: float
) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/workpackages/{id}".format(
        base=base,
        token=token,
        id=id,
    )
    try:
        payload = {"effort": effort, "standarddeviation": standard_deviation}
        res = requests.put(url, json=payload)
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")


def delete_task_from_session(server: Server, token: str, id: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/workpackages/{id}".format(
        base=base,
        token=token,
        id=id,
    )
    try:
        res = requests.delete(url)
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")


def clear_estimate_of_task(server: Server, token: str, id: str) -> NoReturn:
    base = get_base_url(server=server)
    url = "{base}/sessions/{token}/workpackages/{id}/estimate".format(
        base=base,
        token=token,
        id=id,
    )
    try:
        res = requests.delete(url)
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")