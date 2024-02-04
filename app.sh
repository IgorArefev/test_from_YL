#!/bin/bash

if [[ "${1}" == "deploy" ]]; then
  cd menu || exit
  alembic upgrade head
  gunicorn main:menu_app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

elif [[ "${1}" == "test" ]]; then
  pytest -v -s
fi
