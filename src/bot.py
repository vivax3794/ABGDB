import traceback

import discord
from discord.ext import commands
from loguru import logger

from .database import Database
from .database.settings import SETTINGS
from .config import config


class Bot(commands.Bot):
    def __init__(self, db: Database):
        super().__init__(command_prefix="-")

        self.db = db
        self.load_cogs()
        self.settings = SETTINGS

    def run(self) -> None:
        super().run(config.token)

    def load_cogs(self) -> None:
        for cog in config.cogs:
            self.load_extension(f"src.cogs.{cog}")
            logger.info(f"loaded cog: {cog}")

    def unload_all_cogs(self) -> None:
        for cog in config.cogs:
            self.unload_extension(f"src.cogs.{cog}")
            logger.info(f"unloaded cog: {cog}")

    async def get_prefix(self, message: discord.Message) -> str:
        logger.debug(f"getting prefix for message: {message.id}")
        server_id = message.guild.id

        prefix = self.settings["prefix"].get_value(self, server_id)

        return commands.when_mentioned_or(prefix)(self, message)

    async def on_guild_join(self, guild: discord.Guild) -> None:
        self.db.add_server(guild.id)

    async def on_message(self, message: discord.Message) -> None:
        if message.author.id == self.user.id:
            pass  # logger.debug("not replying to my self")
        elif message.guild is None:
            await message.channel.send(
                "sorry but I can not respond to commands in dms since I dont know what prefix to use."
            )
        else:
            await self.process_commands(message)

    async def on_command_error(
        self, ctx: commands.Context, error: commands.CommandError
    ) -> None:
        tb = "".join(traceback.format_exception(None, error, error.__traceback__))
        if ctx.command is not None:
            logger.error(f"command {ctx.command.name} raised an error.")
        else:
            logger.error(error)

        if isinstance(error, commands.CommandNotFound):
            await ctx.send(f"{ctx.author.mention} command not found")
            await ctx.send_help()

        elif isinstance(error, commands.BadArgument) or isinstance(
            error, commands.MissingRequiredArgument
        ):
            logger.error("incorrect arguments given")
            await ctx.send(f"{ctx.author.mention} invalid arguments")
            await ctx.send_help(ctx.command)

        elif isinstance(error, commands.MissingPermissions):
            logger.error("missing permissions")
            missing_permissions = "\n".join(
                f"* {permission}" for permission in error.missing_perms
            )
            await ctx.send(
                f"{ctx.author.mention} you need these permissions to use this command: ```\n{missing_permissions}```"
            )

        elif isinstance(error, commands.CheckFailure):
            logger.info(error)
            await ctx.send(
                f"{ctx.author.mention} you are not allowed to use this command."
            )

        else:
            # if we dont know the error, either it is something we need to cover above or the command causing it is broken.
            logger.error(f"unknow error\n{tb}")
            error_embed = discord.Embed(
                color=discord.Color.red(), title=str(error), description=f"```\n{tb}```"
            )
            await ctx.send(
                f"{ctx.author.mention} unknow error detected.", embed=error_embed
            )
