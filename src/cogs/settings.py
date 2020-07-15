from discord.ext import commands
from ..bot import Bot


class SettingCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx: commands.Context) -> None:
        "return the current prefix"
        prefix = self.bot.db.prefix_get(ctx.guild.id)
        await ctx.send(f"my prefix is: `{prefix}`, but you can always just {self.bot.user.mention} if you are unsure :smile:")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix_change(self, ctx: commands.Context, new_prefix: str) -> None:
        """
        change the current prefix.
        """
        self.bot.db.prefix_update(ctx.guild.id, new_prefix)
        await ctx.send(f"my prefix is now `{new_prefix}`")


def setup(bot: Bot) -> None:
    bot.add_cog(SettingCog(bot))
