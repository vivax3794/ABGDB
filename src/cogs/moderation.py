import typing as t

import discord
from discord.ext import commands
from loguru import logger

from src.bot import Bot


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
        """
        Kick user.
        """
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
        """
        Ban a user
        """
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
        """
        Unban a user.
        """
        await ctx.guild.unban(user)
        await ctx.send(f"unbaned {user.name}")
        modlog_embed = discord.Embed(
                    title=f"{ctx.author.name} unbanned {user.name}",
                    color=discord.Color.orange()
                )
        await self.send_to_modlog(ctx, modlog_embed)

    @commands.guild_only()
    @is_mod
    @commands.command(aliases=["clean"])
    async def purge(self, ctx: commands.Context, ammount: t.Optional[int] = 10, channel: t.Optional[discord.TextChannel] = None):
        if channel is None:
            channel = ctx.channel

        logger.info(f"purging {ammount} messages")
        deleted_messages = await channel.purge(limit=ammount)
        await ctx.send(f"deleted {len(deleted_messages)} messages in {channel.mention}")
        logger.info("purge done")

        modlog_embed = discord.Embed(
                title=f"{ctx.author.name} cleard {len(deleted_messages)} messages in {channel.name}",
                color=discord.Color.red()
                )
        await self.send_to_modlog(ctx, modlog_embed)

    @commands.guild_only()
    @is_mod
    @commands.command()
    async def lock(self, ctx: commands.Context, channel: t.Optional[discord.TextChannel] = None, *, reason: t.Optional[str] = None) -> None:
        if reason is None:
            reason = "no reason given"
        if channel is None:
            channel = ctx.channel

        everyone = ctx.guild.default_role
        overwrites = channel.overwrites_for(everyone)
        overwrites.send_messages = False
        await channel.set_permissions(everyone, overwrite=overwrites)

        lock_embed = discord.Embed(
                    title=":lock: Channel locked by moderator :lock:",
                    color=discord.Color.red(),
                    description=reason
                )
        modlog_embed = discord.Embed(
                    title=f"{ctx.author.name} locked {channel.name}",
                    color=discord.Color.red(),
                    description=reason
                )
        await channel.send(embed=lock_embed)
        await self.send_to_modlog(ctx, modlog_embed)
        await ctx.send(f"locked channel {channel.mention}")

    @commands.guild_only()
    @is_mod
    @commands.command()
    async def unlock(self, ctx: commands.Context, channel: t.Optional[discord.TextChannel] = None, *, reason: t.Optional[str] = None) -> None:
        if reason is None:
            reason = "no reason given"
        if channel is None:
            channel = ctx.channel

        everyone = ctx.guild.default_role
        overwrites = channel.overwrites_for(everyone)
        overwrites.send_messages = None
        await channel.set_permissions(everyone, overwrite=overwrites)

        lock_embed = discord.Embed(
                    title=":unlock:  Channel unlocked by moderator :unlock:",
                    color=discord.Color.green(),
                    description=reason
                )
        modlog_embed = discord.Embed(
                    title=f"{ctx.author.name} unlocked {channel.name}",
                    color=discord.Color.green(),
                    description=reason
                )
        await channel.send(embed=lock_embed)
        await self.send_to_modlog(ctx, modlog_embed)
        await ctx.send(f"unlocked channel {channel.mention}")


def setup(bot: Bot) -> None:
    bot.add_cog(ModCog(bot))
