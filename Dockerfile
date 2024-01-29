FROM python:3.10-slim

RUN pip install poetry==1.7.1

ENV POETRY_VIRTUALENVS_IN_PROJECT=0
ENV POETRY_VIRTUALENVS_CREATE=0

WORKDIR /menu_app

COPY ./pyproject.toml ./poetry.lock ./.env-net ./pytest.ini ./

RUN poetry install --only main --no-root

WORKDIR ./menu

COPY ./menu ./tests ./

ENV PYTHONPATH "${PYTHONPATH}:/menu_app"