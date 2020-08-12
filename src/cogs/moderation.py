import discord
from discord.ext import commands

from ..bot import Bot


is_mod = commands.has_permissions(kick_members=True, ban_members=True)


class ModCog(commands.Cog, name="moderation"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def send_embeds(self, ctx: commands.Context, embed: discord.Embed) -> None:
        modlog: discord.TextChannel = self.bot.settings["modlog"].get_value(self.bot, ctx.guild.id)
        await modlog.send(embed=embed)

    @is_mod
    @commands.guild_only()
    @commands.command()
    async def warn(self, ctx: commands.Context, user: discord.User, *, warning: str) -> None:
        """
        Warn a user.

        sends the user a dm with the warning message
        """
        embed = discord.Embed(
          title=f":warning: You Got a Warning from: {ctx.guild.name} :warning:",
          color=discord.Color.red(),
          description=warning,
        )

        icon_url = ctx.guild.icon_url
        if icon_url != "":
            embed.set_thumbnail(url=icon_url)

        try:
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            sent_dm = False
        else:
            sent_dm = True

        modlog_embed = discord.Embed(
                title=f"{ctx.author.name} warned {user.name}" + ("" if sent_dm else " (could not send dm)"),
                color=discord.Color.red(),
                description=warning
                )
        await self.send_to_modlog(ctx, modlog_embed)
        if sent_dm:
            await ctx.send(f"warned user {user.name}")
        else:
            await ctx.send(f"could not send dm to {user.name}")


def setup(bot: Bot) -> None:
    bot.add_cog(ModCog(bot))
