from dokerc.config.config import (
    Config,
    Server,
    Session,
    User,
)


def update_token(config: Config, token: str) -> Config:
    conf = Config(
        Server(
            config.server.address,
            int(config.server.port),
            config.server.endpoint,
        ),
        User(config.user.name),
        Session(token),
    )
    return conf


def get_base_url(server: Server) -> str:
    if server.port == 0:
        url = "{address}{endpoint}".format(
            address=server.address,
            endpoint=server.endpoint,
        )
    else:
        url = "{address}:{port}{endpoint}".format(
            address=server.address,
            port=server.port,
            endpoint=server.endpoint,
        )
    return url