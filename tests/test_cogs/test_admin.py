from unittest.mock import Mock, patch, AsyncMock

import pytest

from src.cogs.admin import AdminCog


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("admins_list", "user_id", "result"),
    [
        ([123], 123, True),
        ([123], 321, False),
        ([123, 456], 456, True),
        ([123, 456], 789, False),
    ],
)
async def test_admin_check_works_correctly(admins_list, user_id, result):
    with patch("src.cogs.admin.config.admins", admins_list):
        ctx_mock = Mock()
        ctx_mock.author.id = user_id

        self_mock = Mock()
        self_mock.bot.is_owner = AsyncMock(return_value=False)

        assert (await AdminCog.cog_check(self_mock, ctx_mock)) is result


class TestEval:
    def test_code_formatting(self):
        code = """```py
for i in range(10):
    print("hello world")
    ```"""
        formated_code = AdminCog._format_code(None, code)
        assert (
            formated_code
            == """async def func():
    for i in range(10):
        print("hello world")"""
        )
