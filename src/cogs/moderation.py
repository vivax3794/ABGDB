import discord
from discord.ext import commands

from ..bot import Bot


class ModCog(commands.Cog, name="moderation"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def send_to_modlog(self, server_id: int, embed: discord.Embed) -> None:
        modlog: discord.TextChannel = self.bot.settings["modlog"].get_value(self.bot, server_id)
        await modlog.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.add_cog(ModCog(bot))
