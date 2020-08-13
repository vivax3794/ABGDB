import typing as t
import os

import yaml

from loguru import logger


__all__ = ["config"]


class ConfigClass:
    database: str
    cogs: t.List[str]
    admins: t.List[int]
    token: str
    invite: str
    source: str
    ball: t.Dict[str, t.List[str]]
    log_channel: int

    def __init__(self) -> None:
        self.reload_config()

    def load_env_var(self, name: str) -> str:
        var = os.getenv(name)
        if var is None:
            raise KeyError(f"Enviroment var '{name}' not found")

        return var

    def reload_config(self):
        logger.info("loading config.yaml")
        with open("config.yaml") as f:
            self.raw_data = yaml.load(f, Loader=yaml.BaseLoader)

        self.cogs = self.raw_data["cogs"]
        self.admins = [int(id_) for id_ in self.raw_data["admins"]]
        self.invite = self.raw_data["invite"]
        self.source = self.raw_data["source"]
        self.ball = self.raw_data["8ball"]
        self.log_channel = int(self.raw_data["botlogs"])

        # .env vars
        logger.info("loading enviroment vars")
        self.token = self.load_env_var("TOKEN")
        self.database = self.load_env_var("DATABASE_URL")


config = ConfigClass()
