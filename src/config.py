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
    ball: t.Dict[str, t.List[str]]

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

        self.database = self.raw_data["database"]
        self.cogs = self.raw_data["cogs"]
        self.admins = self.raw_data["admins"]
        self.ball = self.raw_data["8ball"]

        # .env vars
        logger.info("loading enviroment vars")
        self.token = self.load_env_var("TOKEN")


config = ConfigClass()
