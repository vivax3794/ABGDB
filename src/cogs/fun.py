import random

import discord
from discord.ext import commands
from loguru import logger

from src.bot import Bot
from src.config import config
from src.utils import reverse_dict


MORSE_CODE_TABLE = {
        "a": ".-",
        "b": "-...",
        "c": "-.-.",
        "d": "-..",
        "e": ".",
        "f": "..-.",
        "g": "--.",
        "h": "....",
        "i": "..",
        "j": ".---",
        "k": "-.-",
        "l": ".-..",
        "m": "--",
        "n": "-.",
        "o": "---",
        "p": ".--.",
        "q": "--.-",
        "r": ".-.",
        "s": "...",
        "t": "-",
        "u": "..-",
        "v": "...-",
        "w": ".--",
        "x": "-..-",
        "y": "-.--",
        "z": "--..",
        ".": "-.-..",
        ",": "--..--",
        "?": "..--..",
        "/": "-..-.",
        "@": ".--.-.",
        "1": ".----",
        "2": "..---",
        "3": "...--",
        "4": "....-",
        "5": ".....",
        "6": "-....",
        "7": "--...",
        "8": "---..",
        "9": "----.",
        "0": "-----",
        " ": "/"
    }


class FunCog(commands.Cog, name="fun"):  # type: ignore
    def __init__(self, bot: Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command(name="8ball")
    async def ball(self, ctx: commands.Context) -> None:
        """
        Ask the ball your questions and it shall respond.
        """
        mood = random.choice(["yes", "no", "maybe"])
        lines = config.ball[mood]
        line = random.choice(lines)
        await ctx.send(line)

    @commands.group(aliases=["morse-code"], invoke_without_command=True)
    async def morse(self, ctx: commands.Context):
        """
        encode and decode morse code!
        """
        await ctx.send_help(self.morse)

    @morse.command(aliases=["e"])
    async def encode(self, ctx: commands.Context, *, message: str) -> None:
        """
        encode a morse code message.
        """
        try:
            morse_code_message = " ".join(map(MORSE_CODE_TABLE.__getitem__, message.lower()))
        except KeyError:
            await ctx.send("unknow characther in message.")
        else:
            await ctx.send(f"`{morse_code_message}`")

    @morse.command(aliases=["d"])
    async def decode(self, ctx: commands.Context, *, morse_code: str) -> None:
        """
        Decode a morse code message.
        """
        reversed_table = reverse_dict(MORSE_CODE_TABLE)

        try:
            message = "".join(map(reversed_table.__getitem__, morse_code.split()))
        except KeyError as e:
            logger.info(str(e))
            await ctx.send("unknow symbol")
        else:
            allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=False)
            await ctx.send(message, allowed_mentions=allowed_mentions)


def setup(bot: Bot) -> None:
    bot.add_cog(FunCog(bot))
