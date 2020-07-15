from unittest.mock import patch

from src import utils


def test_spy() -> None:
    class Foo(utils.Spy):
        def __init__(self) -> None:
            self.a = 1

    with patch("src.utils.logger") as LoggerMock:
        assert Foo().a == 1
        LoggerMock.debug.called_once_with("[SPY] Foo.a")
