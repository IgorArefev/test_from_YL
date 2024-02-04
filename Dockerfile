FROM python:3.10-slim

RUN pip install poetry==1.7.1

WORKDIR /menu_app

COPY ./pyproject.toml ./poetry.lock ./dev.env ./test_dev.env ./app.sh ./pytest.ini ./

RUN chmod a+x ./*.sh
RUN poetry config virtualenvs.create false
RUN poetry install --no-ansi

COPY ./menu /menu_app/menu
COPY ./tests /menu_app/tests

ENV PYTHONPATH "${PYTHONPATH}:/menu_app"
