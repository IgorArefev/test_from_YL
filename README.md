# Система меню
### Тестовое задание от Ylab


[![python](https://cdn.coral.team/images/technologies/python.svg)](https://www.python.org/)
[![fastapi](https://houdoukyokucho.com/wp-content/uploads/2022/09/FastAPI-320x180.png)](https://fastapi.tiangolo.com/)


## Описание

В проекте реализовано REST API по работе с меню ресторана.
Все CRUD операции.
У меню есть подменю, которые к нему привязаны. У подменю есть блюда.

Использованы следующие технологии:

- Python 3.10.5
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Pydantic 2.5.3
- Alembic 1.13.1
- PostgreSQL 15.1
- Docker


## Как запустить?

### Для запуска потребуется докер

1. Клонируем проект:
```
git clone git@github.com:IgorArefev/test_from_YL.git
```
2. Применяем миграции:
```
alembic revision --autogenerate -m "You're comment here"
```
В корневом каталоге запускаем проект командой:
```
docker-compose --env-file ./dev.env up
```

## Тестируем

- Через Postman с помощью json файлов из папки tests
- В локальной среде командой
```
pytest -v
```
- Через doker
```
docker-compose --env-file ./test_dev.env -f docker-compose-test.yml up
```


Так же ознакомится с функционалом можно через SWAGGER
- в локальной среде:
```
http://127.0.0.1:8000/docs
```
- в запущеном doker
```
http://localhost:8000/docs
```


## Запрос в БД для подсчета подменю и блюд по адресу
```
menu/models/menu.py  :19 строка
```
