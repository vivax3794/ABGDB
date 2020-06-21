from src.database import Database

import discord
from discord.ext import commands
from loguru import logger

from config_SECRET import COGS
class Bot(commands.Bot):
    def __init__(self, db: Database):
        super().__init__(command_prefix="-")

        self.db = db
        self.load_cogs()

    def load_cogs(self) -> None:
        for cog in COGS:
            self.load_extension(f"src.cogs.{cog}")
            logger.info(f"loaded cog: {cog}")

    async def get_prefix(self, message: discord.Message) -> str:
        server_id = message.guild.id
        prefix = self.db.prefix_get(server_id)

        return prefix

    async def on_guild_join(self, guild: discord.Guild) -> None:
        self.db.prefix_add(guild.id, "!")
