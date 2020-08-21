from typing import Optional

import discord
from discord.ext import commands

from src.bot import Bot


class SettingsCog(commands.Cog, name="config"):  # type: ignore
    """
    Configure and see settings about the bot.
    """
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    async def list_settings(self, ctx: commands.Context) -> None:
        embed = discord.Embed(
                title="settings",
                color=discord.Color.green(),
                description="\n".join(
                    f"**{index + 1}.** {setting}"
                    for index, setting in enumerate(self.bot.settings.keys())
                    )
                )

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.group(name="settings", aliases=["config"], invoke_without_command=True)
    async def settings_group(self, ctx: commands.Context, setting: Optional[str] = None) -> None:
        """
        List all settings

        give a setting to display it's value.
        """
        if setting is None:
            await self.list_settings(ctx)
            return

        setting = setting.lower()

        if setting not in self.bot.settings:
            embed = discord.Embed(
                    title="Not Found",
                    color=discord.Color.red(),
                    description=f"`{setting}` is not a valid setting"
                    )

        else:
            value = self.bot.settings[setting].get_value(self.bot, ctx.guild.id)
            embed = discord.Embed(
                    title=setting,
                    color=discord.Color.green(),
                    description=f"```\n{value}```"
                    )

        await ctx.send(embed=embed)

    @commands.has_permissions(manage_guild=True)
    @settings_group.command()
    async def change(self, ctx: commands.Context, setting_name: str, *, new_value: str) -> None:
        """
        Change the value of a setting.
        """
        setting_name = setting_name.lower()

        if setting_name not in self.bot.settings:
            embed = discord.Embed(
                    title="Not Found",
                    color=discord.Color.red(),
                    description=f"`{setting_name}` is not a valid setting"
                    )
        else:
            setting = self.bot.settings[setting_name]
            if setting.discord_convertor is not None:
                new_value = await setting.discord_convertor.convert(ctx, new_value)

            try:
                setting.set_value(self.bot, ctx.guild.id, new_value)
            except ValueError:
                embed = discord.Embed(
                        title="Invalid setting value",
                        color=discord.Color.red(),
                        description=f"```\n{new_value}``` is not a valid setting for `{setting_name}`"
                        )
            else:
                embed = discord.Embed(
                        title="Setting changed",
                        color=discord.Color.green(),
                        description=f"`{setting_name}` changed to ```\n{new_value}```"
                        )

        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.has_permissions(manage_guild=True)
    @commands.command(name="change-setting", help=change.help)
    async def change_setting_command(self, ctx: commands.Context, setting: str, *, new_value: str) -> None:
        await self.change.callback(self, ctx, setting, new_value=new_value)


def setup(bot: Bot) -> None:
    bot.add_cog(SettingsCog(bot))
