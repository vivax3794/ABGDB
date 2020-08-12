import typing as t

import discord
from discord.ext import commands

from ..bot import Bot


is_mod = commands.has_permissions(kick_members=True, ban_members=True)


class ModCog(commands.Cog, name="moderation"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def send_to_modlog(self, ctx: commands.Context, embed: discord.Embed) -> None:
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

        embed.set_thumbnail(url=ctx.guild.icon_url)

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

    @commands.guild_only()
    @is_mod
    @commands.command()
    async def kick(self, ctx: commands.Context, user: discord.Member, *, reason: t.Optional[str]) -> None:
        if reason is None:
            reason = "No reason given."

        kick_embed = discord.Embed(
                title=f"You were kicked from {ctx.guild.name}",
                color=discord.Color.red(),
                description=reason,
                )
        kick_embed.set_thumbnail(url=ctx.guild.icon_url)

        try:
            await user.send(embed=kick_embed)
        except discord.errors.Forbidden:
            pass

        await user.kick(reason=reason)

        modlog_embed = discord.Embed(
                title=f"{ctx.author.name} kicked {user.name}",
                color=discord.Color.red(),
                description=reason
                )

        await self.send_to_modlog(ctx, modlog_embed)
        await ctx.send(f"kicked {user.name}")

    @commands.guild_only()
    @is_mod
    @commands.command()
    async def ban(self, ctx: commands.Context, user: discord.Member, *, reason: t.Optional[str]) -> None:
        if reason is None:
            reason = "No Reason Given"

        ban_embed = discord.Embed(
                title=f"You were ban from {ctx.guild.name}",
                color=discord.Color.red(),
                description=reason,
                )
        ban_embed.set_thumbnail(url=ctx.guild.icon_url)

        try:
            await user.send(embed=ban_embed)
        except discord.errors.Forbidden:
            pass

        await user.ban(reason=reason)

        modlog_embed = discord.Embed(
                title=f"{ctx.author.name} banned {user.name}",
                color=discord.Color.red(),
                description=reason
                )

        await self.send_to_modlog(ctx, modlog_embed)
        await ctx.send(f"banned user {user.name}")

    @commands.guild_only()
    @is_mod
    @commands.command(aliases=["un-ban"])
    async def unban(self, ctx: commands.Context, user: discord.User) -> None:
        await ctx.guild.unban(user)
        await ctx.send(f"unbaned {user.name}")
        modlog_embed = discord.Embed(
                    title=f"{ctx.author.name} unbanned {user.name}",
                    color=discord.Color.orange()
                )
        await self.send_to_modlog(ctx, modlog_embed)


def setup(bot: Bot) -> None:
    bot.add_cog(ModCog(bot))
