from typing import Dict, Optional, List

from ..bot import Bot
from ..utils import Spy

import discord
from discord.ext import commands


MAPPING = Dict[Optional[commands.Cog], List[commands.Command]]


class HelpCommand(commands.HelpCommand, Spy):
    """show this"""

    async def send_bot_help(self, mapping: MAPPING) -> None:
        embed = discord.Embed(title="help", color=discord.Color.blue())
        for cog, command_list in mapping.items():
            if cog is None:
                category = "Not Grouped"
            else:
                category = cog.qualified_name.replace("Cog", "")

            allowed_commands = await self.filter_commands(command_list)
            embed.add_field(
                name=category,
                value="\n".join(
                    f"`{command.name}` - {command.brief}"
                    for command in allowed_commands
                ),
            )

        channel: discord.abc.Messageable = self.get_destination()
        await channel.send(embed=embed)


def setup(bot: Bot) -> None:
    bot.remove_command("help")
    bot.help_command = HelpCommand()
