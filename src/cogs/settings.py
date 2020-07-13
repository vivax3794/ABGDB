from discord.ext import commands
from ..bot import Bot


class SettingCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def prefix(self, ctx: commands.Context) -> None:
        prefix = self.bot.db.prefix_get(ctx.guild.id)
        await ctx.send(f"my prefix is: `{prefix}`, but you can always just {self.bot.user.mention} if you are unsure :smile:")


def setup(bot: Bot) -> None:
    bot.add_cog(SettingCog(bot))
