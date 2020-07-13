from unittest.mock import Mock, patch
import asyncio

import pytest

from src.cogs.admin import AdminCog


@pytest.mark.parametrize("admins_list, user_id, result",
                         [
                            ([123], 123, True),
                            ([123], 321, False),
                            ([123, 456], 456, True),
                            ([123, 456], 789, False)
                         ])
def test_admin_check_works_correctly(admins_list, user_id, result):
    with patch("src.cogs.admin.ADMINS", admins_list):
        ctx = Mock()
        author = Mock()

        author.id = user_id
        ctx.author = author

        self_mock = Mock()
        self_mock.bot.is_owner.return_value = False

        assert asyncio.run(AdminCog.cog_check(self_mock, ctx)) is result


class TestEval:
    def test_code_formatting(self):
        code = """```py
for i in range(10):
    print("hello world")
    ```"""
        formated_code = AdminCog._format_code(None, code)
        assert formated_code == """async def func():
    for i in range(10):
        print("hello world")"""
