FROM python:3.10-slim
RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=0
ENV POETRY_VIRTUALENVS_CREATE=0

WORKDIR /menu

COPY ./pyproject.toml ./poetry.lock ./

RUN poetry install --only main --no-root

COPY ./menu .

CMD gunicorn main:menu_app --bind=0.0.0.0:8000