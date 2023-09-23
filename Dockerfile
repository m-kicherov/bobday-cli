FROM python:3.10-alpine3.18

WORKDIR /src

RUN pip3 install poetry

RUN poetry config virtualenvs.create false

COPY . /src

RUN poetry install

ENTRYPOINT ["poetry", "run"]