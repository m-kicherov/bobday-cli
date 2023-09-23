import typing as t
import tempfile
from pytest import fixture

from bobday_app import App


@fixture
def app() -> t.Generator[App, None, None]:
    with tempfile.NamedTemporaryFile() as tmp_file:
        yield App("user", "password", log_file=tmp_file.name)
