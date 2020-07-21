from discord.ext import commands
from ..bot import Bot


class SettingsCog(commands.Cog, name="settings"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot


def setup(bot: Bot) -> None:
    bot.add_cog(SettingsCog(bot))
