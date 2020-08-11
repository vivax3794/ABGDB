import typing as t

from loguru import logger


class Spy:
    """
    Logs attribute lookup on it self, used during debug and not in the actuall code.
    """

    def __getattribute__(self, value: str) -> t.Any:
        if value.startswith("__") and value.endswith("__"):
            # ignore dunder methods
            return object.__getattribute__(self, value)

        logger.log("SPY", f"{self.__class__.__name__}.{value}")
        attr = object.__getattribute__(self, value)

        return attr


K = t.TypeVar("K")
V = t.TypeVar("V")


def reverse_dict(data: t.Dict[K, V]) -> t.Dict[V, K]:
    new_dict: t.Dict[V, K] = {}
    for key, value in data.items():
        if value in new_dict:
            logger.warning(f"overwrtting value for key {value}: {new_dict[value]} -> {key}")

        new_dict[value] = key

    return new_dict
