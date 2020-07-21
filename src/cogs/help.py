from typing import Dict, Optional, List

from ..bot import Bot
from ..utils import Spy

import discord
from discord.ext import commands


MAPPING = Dict[Optional[commands.Cog], List[commands.Command]]


class HelpCommand(commands.HelpCommand, Spy):
    """show this"""

    async def _send_embed(self, embed: discord.Embed) -> None:
        """
        Send an embed to the help destionation
        """
        destionation: discord.abc.Messageable = self.get_destination()
        await destionation.send(embed=embed)

    async def send_bot_help(self, mapping: MAPPING) -> None:
        embed = discord.Embed(title="help", color=discord.Color.blue())
        for cog, command_list in mapping.items():
            if cog is None:
                category = "Not Grouped"
            else:
                category = cog.qualified_name.replace("Cog", "")

            allowed_commands = await self.filter_commands(command_list)
            if len(allowed_commands) == 0:
                continue

            embed.add_field(
                name=category,
                value="\n".join(
                    f"`{command.name}` - {command.short_doc}"
                    for command in allowed_commands
                ),
                inline=False
            )

        await self._send_embed(embed)

    async def send_command_help(self, command: commands.Command) -> None:
        embed = discord.Embed(
                title=command.qualified_name,
                description=f"```{self.get_command_signature(command)}```\n{command.help}",
                color=discord.Color.blue()
                )

        await self._send_embed(embed)

    async def send_cog_help(self, cog: commands.Cog) -> None:
        allowed_commands = await self.filter_commands(cog.get_commands())
        embed = discord.Embed(
                title=cog.qualified_name.replace("Cog", ""),
                description="\n".join(
                    f"`{command.name}` - {command.short_doc}"
                    for command in allowed_commands
                    )
                )
        await self._send_embed(embed)


def setup(bot: Bot) -> None:
    bot.remove_command("help")
    bot.help_command = HelpCommand()
