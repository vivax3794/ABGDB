import random

from discord.ext import commands
from loguru import logger

from ..bot import Bot
from ..config import config


class FunCog(commands.Cog, name="fun"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name="8ball")
    async def ball(self, ctx: commands.Context) -> None:
        mood = random.choice(["yes", "no", "maybe"])
        lines = config.ball[mood]
        line = random.choice(lines)
        await ctx.send(line)


def setup(bot: Bot) -> None:
    bot.add_cog(FunCog(bot))
