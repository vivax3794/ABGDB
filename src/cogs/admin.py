from discord.ext import commands

from src.bot import Bot
from config_SECRET import ADMINS


class AdminCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.id in ADMINS

    @commands.command()
    async def eval(self, ctx: commands.Context, *, code: str) -> None:
        code = self._format_code(code)
        globals_ = {
                "ctx": ctx,
                "bot": self.bot,
                "db": self.bot.db,
                }
        exec(code, globals_)
        await globals_["func"]()

    def _format_code(self, code: str) -> str:
        lines = code.splitlines()[1:-1]

        formatted_lines = ["async def func():"]
        for line in lines:
            formatted_lines.append("    " + line)

        code = "\n".join(formatted_lines)

        return code


def setup(bot: Bot) -> None:
    bot.add_cog(AdminCog(bot))
