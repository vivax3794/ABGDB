from contextlib import redirect_stdout
from io import StringIO

from discord.ext import commands

from ..bot import Bot
from config import ADMINS


class AdminCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.id in ADMINS or await self.bot.is_owner(ctx.author)

    @commands.command(name="eval")
    async def eval_command(self, ctx: commands.Context, *, code: str) -> None:
        """
        Run the given python code.

        it must be in this format!!!
        !eval ```py
        print("hello world")
        ```

        that last newline is very important
        """
        code = self._format_code(code)
        globals_ = {
            "ctx": ctx,
            "bot": self.bot,
            "db": self.bot.db,
        }

        output = StringIO()
        with redirect_stdout(output):
            async with ctx.typing():
                exec(code, globals_)
                await globals_["func"]()

        await ctx.send(f"```\n{output.getvalue()}```")

    def _format_code(self, code: str) -> str:
        lines = code.splitlines()[1:-1]

        formatted_lines = ["async def func():"]
        for line in lines:
            formatted_lines.append("    " + line)

        code = "\n".join(formatted_lines)

        return code


def setup(bot: Bot) -> None:
    bot.add_cog(AdminCog(bot))
