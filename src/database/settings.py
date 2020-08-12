from abc import ABC, abstractmethod
from typing import Any, TypeVar, Generic, Dict

import discord
from discord.ext import commands


class Setting(ABC):
    discord_convertor = None
    """
    Represents a setting and has functions to interact with it.
    these are the args for all the functions you should overwrite (validate_input, get_value, set_value)
    args:
        bot - Bot: the bot in case it needs to fetch something from the discord api
        server_id - id: the server id of the server this setting is activated from.
    """
    @abstractmethod
    def _validate_input(self, bot, server_id: int, value: Any) -> bool:
        """
        Check if the input is valid

        args:
            value - str: the value that should be checked
        """
        return NotImplemented

    @abstractmethod
    def get_value(self, bot, server_id: int) -> Any:
        """
        Return the current value for this setting
        """
        return NotImplemented

    @abstractmethod
    def _set_value_core(self, bot, server_id: int, new_value: Any) -> None:
        """
        Set a new value for the settin
        validating the input is done before being passed to this function

        args:
            new_value - str: the new value to set the setting
        """
        return NotImplemented

    def set_value(self, bot, server_id: int, new_value: Any) -> None:
        if self._validate_input(bot, server_id, new_value):
            self._set_value_core(bot, server_id, new_value)

        else:
            raise ValueError(f"{new_value!r} failed validator for {self.__class__.__name__}")


T = TypeVar("T")


class ConverterSetting(Setting, Generic[T]):
    """
    Convert input
    """
    @abstractmethod
    def _converter(self, value: str) -> T:
        return NotImplemented

    def _validate_input(self, bot, server_id: int, value: str) -> bool:
        try:
            self._converter(value)
        except ValueError:
            return False
        else:
            return True

    @abstractmethod
    def _set_value_core(self, bot, server_id: int, new_value: T) -> None:  # type: ignore[override]
        return NotImplemented

    def set_value(self, bot, server_id: int, new_value: str) -> None:
        if self._validate_input(bot, server_id, new_value):
            self._set_value_core(bot, server_id, self._converter(new_value))

        else:
            raise ValueError(f"{new_value!r} failed validator for {self.__class__.__name__}")


class BoolConvertorSetting(ConverterSetting):
    def _converter(self, value: str) -> bool:
        """
        Convert a value to a bool.
        """
        value = value.lower().strip()
        if value in {"y", "yes", "true"}:
            return True
        elif value in {"n", "no", "false"}:
            return False
        else:
            raise ValueError(f"{value} is not a valid resonse")


class PrefixSetting(Setting):
    def _validate_input(self, bot, server_id: int, value: str) -> bool:
        return not value.isspace()

    def get_value(self, bot, server_id: int) -> str:
        return bot.db.get_setting("prefix", server_id)

    def _set_value_core(self, bot, server_id: int, value: str) -> None:
        return bot.db.update_setting(server_id, "prefix", value)


class ModlogSetting(Setting):
    discord_convertor = commands.converter.TextChannelConverter()

    def _validate_input(self, bot, server_id: int, value: discord.TextChannel) -> bool:
        return True

    def get_value(self, bot, server_id: int) -> discord.TextChannel:
        channel_id = bot.db.get_setting("modlog", server_id)

        if channel_id == 0 or channel_id is None:
            return None

        channel = bot.get_channel(channel_id)
        return channel

    def _set_value_core(self, bot, server_id: int, channel: discord.TextChannel) -> None:  # type: ignore[override]
        bot.db.update_setting(server_id, "modlog", channel.id)


SETTINGS: Dict[str, Setting] = {
        "prefix": PrefixSetting(),
        "modlog": ModlogSetting()
        }
