import random
from discord.ext import commands

from ..bot import Bot
from ..config import config


MorseCodeTable = {
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
        "r": ".--.",
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
            morse_code_message = " ".join(map(MorseCodeTable.__getitem__, message))
        except KeyError:
            await ctx.send("unknow characther in message.")
        else:
            await ctx.send(f"`{morse_code_message}`")


def setup(bot: Bot) -> None:
    bot.add_cog(FunCog(bot))
