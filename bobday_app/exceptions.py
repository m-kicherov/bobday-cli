import typing as t
from functools import wraps
from httpx import TimeoutException, NetworkError

__all__ = [
    "TimeoutException",
    "NetworkError",
    "ApplicationError",
    "HttpError",
    "exception_handler",
]


class ApplicationError(BaseException):
    message: str

    def __init__(self, message: str = "Базовое исключение приложения"):
        self.message = message

    def __str__(self):
        return self.message


class HttpError(ApplicationError):
    code: int

    def __init__(self, code: int, message: str = "Ошибка при выполнении запроса"):
        super().__init__(message)
        self.code = code

    def __str__(self):
        return f"{self.message} : {self.code}"


@t.overload
def exception_handler(
    tracking: tuple[type[KeyError], type[TypeError]],
    handler: t.Type[ApplicationError]
):
    ...


@t.overload
def exception_handler(
    tracking: tuple[type[TimeoutException], type[NetworkError], type[HttpError]],
    handler: t.Type[ApplicationError]
):
    ...


@t.overload
def exception_handler(
    tracking: tuple[type[OSError]],
    handler: t.Type[ApplicationError]
):
    ...


def exception_handler(tracking, handler) -> t.Callable:
    def decorator(func: t.Callable) -> t.Callable:
        @wraps(func)
        def decorated_function(*args: t.Any, **kwargs: t.Any) -> t.Any:
            try:
                return func(*args, **kwargs)
            except tracking as ex:
                raise handler(str(ex)) from ex
        return decorated_function
    return decorator
