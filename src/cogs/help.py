from typing import Dict, Optional, List

from src.bot import Bot
from loguru import logger

import discord
from discord.ext import commands


MAPPING = Dict[Optional[commands.Cog], List[commands.Command]]


class HelpCommand(commands.HelpCommand):
    """show this"""

    async def send_embed(self, embed: discord.Embed) -> None:
        """
        Send an embed to the help destionation
        """
        destionation: discord.abc.Messageable = self.get_destination()
        await destionation.send(embed=embed)

    async def send_bot_help(self, mapping: MAPPING) -> None:
        embed = discord.Embed(title="help", color=discord.Color.blue(), description="use `<prefix>help [category]` to see the commands")
        for cog, command_list in mapping.items():
            allowed_commands = await self.filter_commands(command_list)
            if len(allowed_commands) == 0:
                continue

            if cog is None:
                embed.add_field(
                    name="other",
                    value="\n".join(
                        f"`{command.qualified_name}` - {command.short_doc}"
                        for command in allowed_commands
                    ),
                    inline=False
                )
            else:
                embed.add_field(
                    name=cog.qualified_name,
                    value=cog.description,
                    inline=False
                )

        await self.send_embed(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = discord.Embed(
                title=command.qualified_name,
                description=f"```{self.get_command_signature(command)}```\n{command.help}",
                color=discord.Color.blue()
                )

        await self.send_embed(embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        allowed_commands = await self.filter_commands(cog.get_commands())
        embed = discord.Embed(
                title=cog.qualified_name,
                description="\n".join(
                    f"`{command.name}` - {command.short_doc}"
                    for command in allowed_commands
                    ),
                color=discord.Color.blue()
                )
        await self.send_embed(embed)

    async def send_group_help(self, group: commands.Group) -> None:
        allowed_commands = await self.filter_commands(group.commands)
        signature = self.get_command_signature(group)

        embed = discord.Embed(
                title=group.qualified_name,
                description=f"""```\n{signature}```{group.help}""",
                color=discord.Color.blue()
                )

        if len(allowed_commands) != 0:
            embed.add_field(
                    name="Sub Commands",
                    inline=False,
                    value="\n".join(
                        f"`{command.name}` - {command.short_doc}"
                        for command in allowed_commands
                        )
                    )

        await self.send_embed(embed)

    async def send_error_message(self, error: str) -> None:
        embed = discord.Embed(
                color=discord.Color.red(),
                description=error
                )

        await self.send_embed(embed)


def setup(bot: Bot) -> None:
    bot.remove_command("help")
    bot.help_command = HelpCommand()
