from know_nepal.config import db_config

tortoise_config = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.asyncpg",
            "credentials": {
                "database": db_config.db,
                "host": db_config.host,
                "password": db_config.password,
                "port": db_config.port,
                "user": db_config.user,
            },
        }
    },
    "apps": {
        "main": {
            "models": [
                "know_nepal.core.models",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    },
}
