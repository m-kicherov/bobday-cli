from __future__ import annotations

from logging import getLogger, Logger
from datetime import datetime
from itertools import groupby

from .rest_client import RestClient
from .exceptions import ApplicationError, exception_handler
from .constants import DEFAULT_OUTPUT_FILE_NAME, DEFAULT_REST_HEADERS, DEFAULT_URL


class App:
    logger: Logger = getLogger("ApplicationLogger")
    log_file: str
    _data: dict | None = None

    def __init__(self, user: str, password: str, *, log_file: str = DEFAULT_OUTPUT_FILE_NAME):
        self.rest = RestClient(DEFAULT_URL, (user, password), DEFAULT_REST_HEADERS)
        self.log_file = log_file

    def get(self) -> App:
        self._data = self.rest('GET')
        return self

    def post(self) -> App:
        self.rest('POST', data=self.data)
        return self

    @exception_handler((KeyError, TypeError), ApplicationError)
    def group_by_department(self) -> App:
        self._data = {
            department["id"]: {
                "department_name": department["department_name"],
                "employees": [
                    {
                        "name": employee["name"],
                        "age": employee["age"]
                    } for employee in employees
                ],
            }
            for department, employees in groupby(
                self.data["employees"], key=lambda x: x["department"]
            )
        }
        return self

    @exception_handler((OSError,), ApplicationError)
    def save_to_file(self) -> App:
        with open(self.log_file, 'a') as file:
            file.write(f'{datetime.utcnow().isoformat()} - {self.data}\n')
        self.logger.info('Данные сохранены в %s', self.log_file)
        return self

    @property
    def data(self):
        if self._data is None:
            raise ApplicationError('Нет данных')
        return self._data
