import sys

import discord
from discord.ext import commands

from ..bot import Bot
from ..config import config


class InfoCog(commands.Cog, name="info"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def info(self, ctx: commands.Context) -> None:
        info_embed = discord.Embed(title="Bot Info", color=discord.Color.blue())

        # get info
        system = sys.platform
        invite = config.invite
        source = config.source

        info_embed.description = f"I am running on a {system} system. \nYou can invite me [here]({invite}), and my source code is [here]({source})"

        await ctx.send(embed=info_embed)


def setup(bot: Bot) -> None:
    bot.add_cog(InfoCog(bot))
