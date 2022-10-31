from pydantic import BaseSettings


class BotConfig(BaseSettings):
    token: str
    github_token: str
    test_guilds: list[int]
    role_id: str
    github_org: str

    class Config:
        env_file = ".env"


bot_config = BotConfig()
