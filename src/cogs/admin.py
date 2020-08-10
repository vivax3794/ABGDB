from contextlib import redirect_stdout
from io import StringIO

from discord.ext import commands
from loguru import logger

from ..bot import Bot
from ..config import config


class AdminCog(commands.Cog, name="admin"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def cog_check(self, ctx: commands.Context) -> bool:
        return ctx.author.id in config.admins or await self.bot.is_owner(ctx.author)

    @commands.command(name="eval")
    async def eval_command(self, ctx: commands.Context, *, code: str) -> None:
        """
        Run the given python code.

        it must be in this format!!!
        > !eval \\`\\`\\`py
        > print("hello world")
        > \\`\\`\\`

        that last newline is very important
        """
        code = self._format_code(code)
        globals_ = {
            **globals(),
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

    @commands.command(aliases=["r-cog"])
    async def unload(self, ctx: commands.Context, cog: str):
        """
        unload a cog.

        use '*' to unload all.
        """
        if cog == "*":
            self.bot.unload_all_cogs()
            await ctx.send("unloaded all cogs")
        else:
            self.bot.unload_extension(f"src.cogs.{cog}")
            logger.info(f"unloaded cog: {cog}")
            await ctx.send(f"unloaded cog {cog}")

    @commands.command(aliases=["a-cog"])
    async def load(self, ctx: commands.Context, cog: str):
        """
        load a cog.

        use '*' to load all.
        """
        if cog == "*":
            self.bot.load_cogs()
            await ctx.send("loaded all cogs")
        else:
            self.bot.load_extension(f"src.cogs.{cog}")
            logger.info(f"unloaded cog: {cog}")
            await ctx.send(f"loaded cog {cog}")

    @commands.command(aliases=["restart"])
    async def reload(self, ctx: commands.Context, cog: str) -> None:
        """
        reload a cog.

        use '*' to reload all.
        you can pass 'config' to reload the config.
        """
        if cog == "*":
            self.bot.unload_all_cogs()
            self.bot.load_cogs()
            await ctx.send("reloaded all cogs")
        elif cog == "config":
            config.reload_config()
            await ctx.send("reloaded the config.yaml")
        else:
            self.bot.unload_extension(f"src.cogs.{cog}")
            self.bot.load_extension(f"src.cogs.{cog}")
            logger.info(f"reloaded cog: {cog}")
            await ctx.send(f"reloaded cog: {cog}")


def setup(bot: Bot) -> None:
    bot.add_cog(AdminCog(bot))
