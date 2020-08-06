from typing import Type
from unittest import mock
import copy

from src.database import settings

from pytest import raises


def generate_setting_cls(validate_return: bool) -> Type[settings.Setting]:
    class Foo(settings.Setting):
        set_was_called = False

        @staticmethod
        def _validate_input(*args) -> bool:
            return validate_return

        @staticmethod
        def get_value(*args) -> None:
            pass

        @staticmethod
        def _set_value_core(*args) -> None:
            Foo.set_was_called = True

    return Foo


class TestGenerateSetting:
    def test_true(self) -> None:
        """
        Test code needs testing :P
        """
        foo = generate_setting_cls(True)
        assert foo()._validate_input(None, None, None) is True  # type: ignore

    def test_false(self) -> None:
        """
        Test code needs testing :P
        """
        foo = generate_setting_cls(False)
        assert foo()._validate_input(None, None, None) is False  # type: ignore


class TestValidate:
    def test_validate_pass(self) -> None:
        Foo = generate_setting_cls(True)
        bar = Foo()

        bar.set_value(None, None, None)  # type: ignore

        assert Foo.set_was_called, "Foo.set_value_core was not called"  # type: ignore

    def test_validate_fail(self) -> None:
        Foo = generate_setting_cls(False)
        bar = Foo()

        with raises(ValueError):
            bar.set_value(None, None, None)  # type: ignore
        assert not Foo.set_was_called, "Foo.set_value_core was called"  # type: ignore


class TestConvertor:
    def setup(self):
        self.cls = copy.deepcopy(settings.ConverterSetting)
        self.cls._set_value_core = mock.Mock()
        self.cls.get_value = mock.Mock()
        self.cls.__abstractmethods__ = set()

    def test_convertor_sucess(self):
        self.cls._converter = mock.Mock(return_value="abc")
        Foo = self.cls()

        Foo.set_value(None, None, None)  # type: ignore

        Foo._set_value_core.assert_called_once_with(None, None, "abc")

    def test_convertor_fail(self):
        # results in ValueError
        self.cls._converter = lambda s, v: max([])
        Foo = self.cls()

        with raises(ValueError):
            Foo.set_value(None, None, None)  # type: ignore
        Foo._set_value_core.assert_not_called()
