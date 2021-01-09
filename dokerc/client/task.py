import json
import requests
from typing import NamedTuple, NoReturn
from dokerc.config.config import Server


class TaskError(RuntimeError):
    pass


class Task(NamedTuple):
    id: str
    summary: str
    effort: float
    standard_deviation: float


def get_tasks_from_session(server: Server, token: str) -> [Task]:
    url = "{address}:{port}{endpoint}/sessions/{token}/workpackages".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
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
    url = "{address}:{port}{endpoint}/sessions/{token}/workpackages".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
    )
    try:
        res = requests.post(url, data={"id": id, "summary": summary})
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")


def update_task_of_session(
    server: Server, token: str, id: str, effort: float, standard_deviation: float
) -> NoReturn:
    url = "{address}:{port}{endpoint}/sessions/{token}/workpackages/{id}".format(
        address=server.address,
        port=server.port,
        endpoint=server.endpoint,
        token=token,
        id=id,
    )
    try:
        res = requests.put(
            url, data={"effort": effort, "standarddeviation": standard_deviation}
        )
        if res.status_code != 200:
            values = res.json()
            raise TaskError(values["reason"])

    except requests.exceptions.ConnectionError:
        raise TaskError("Unable to reach backend")