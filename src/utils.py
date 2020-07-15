from typing import Any

from loguru import logger


class Spy:
    def __getattribute__(self, value: str) -> Any:
        if value.startswith("__") and value.endswith("__"):
            # ignore dunder methods
            return object.__getattribute__(self, value)

        logger.debug(f"[SPY] {self.__class__.__name__}.{value}")
        return object.__getattribute__(self, value)
