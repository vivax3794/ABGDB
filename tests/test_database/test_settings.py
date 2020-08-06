from typing import Type

from src.database.settings import Setting

from pytest import raises


def generate_setting_cls(validate_return: bool) -> Type[Setting]:
    class Foo(Setting):
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
