import discord
from discord.ext import commands

from src.bot import Bot
from src.config import config


class LoggingCog(commands.Cog, name="logging"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def send_log(self, *args, **kwargs) -> None:
        log_channel = self.bot.get_channel(config.log_channel)
        await log_channel.send(*args, **kwargs)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        embed = discord.Embed(
                title="joined new server",
                color=discord.Color.green(),
                description=f"joined server {guild.name}"
                )
        await self.send_log(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        embed = discord.Embed(
                title="left server",
                color=discord.Color.red(),
                description=f"left server {guild.name}"
                )
        await self.send_log(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        embed = discord.Embed(
                title="Bot online",
                color=discord.Color.green(),
                )
        await self.send_log(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(LoggingCog(bot))
