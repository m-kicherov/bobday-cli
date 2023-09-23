from datetime import datetime
from unittest.mock import MagicMock, patch

from freezegun import freeze_time
import httpx
from pytest import mark, raises

from bobday_app import App
from bobday_app.exceptions import TimeoutException, NetworkError, HttpError, ApplicationError
from bobday_app.rest_client import RestClient


pytestmark = [
    mark.asyncio,
]


@mark.parametrize(
    "data, expected",
    [
        (
            {
                "employees": [
                    {
                        "name": "John",
                        "age": 30,
                        "department": {"id": 123, "department_name": "Development"},
                    },
                    {
                        "name": "Bob",
                        "age": 41,
                        "department": {"id": 123, "department_name": "Development"},
                    },
                    {
                        "name": "Ivan",
                        "age": 18,
                        "department": {"id": 22, "department_name": "HR"},
                    },
                ]
            },
            {
                123: {
                    "department_name": "Development",
                    "employees": [
                        {"name": "John", "age": 30},
                        {"name": "Bob", "age": 41},
                    ],
                },
                22: {
                    "department_name": "HR",
                    "employees": [{"name": "Ivan", "age": 18}],
                },
            },
        ),
    ],
)
async def test_groub_by(data: dict, expected: dict, app: App):
    with patch.object(RestClient, "__call__", MagicMock(return_value=data)):
        app.get()
        assert app.data == data
        app.group_by_department()
        assert app.data == expected


@freeze_time("2023-01-01")
async def test_save_to_file(app: App):
    app._data = {"test": "test"}
    app.save_to_file()
    with open(app.log_file, "r") as log_file:
        assert log_file.read() == f"{datetime.utcnow().isoformat()} - {app.data}\n"


@mark.parametrize(
    "exception", [
        TimeoutException("test"), NetworkError("test"), HttpError(500)
    ]
)
async def test_get_with_exceptions(exception: Exception, app: App):
    with patch.object(httpx, "request", MagicMock(side_effect=exception)):
        with raises(ApplicationError):
            app.get()
