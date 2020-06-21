from discord.ext import commands
from src.bot import Bot


class SettingCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot


def setup(bot: Bot) -> None:
    bot.add_cog(SettingCog(bot))
