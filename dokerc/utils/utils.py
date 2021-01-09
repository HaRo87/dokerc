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