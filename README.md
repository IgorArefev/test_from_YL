# Система меню
### Тестовое задание от Ylab


[![python](https://cdn.coral.team/images/technologies/python.svg)](https://www.python.org/)
[![fastapi](https://houdoukyokucho.com/wp-content/uploads/2022/09/FastAPI-320x180.png)](https://fastapi.tiangolo.com/)


## Описание

В проекте реализовано REST API по работе с меню ресторана.
Все CRUD операции.
У меню есть подменю, которые к нему привязаны. У подменю есть блюда.

Использованы следующие технологии:

- Python 3.11.4
- FastAPI 0.109.0
- SQLAlchemy 2.0.25
- Pydantic 2.5.3
- Alembic 1.13.1
- PostgreSQL 16

## Как запустить?

1. Клонируем проект:
```
git clone git@github.com:IgorArefev/test_from_YL.git
```
2. Устанавливаем зависимости:
```
poetry install
```
3. В .env записываем данные для подключения к БД PostgreSQL
```
DB_NAME=
DB_PORT=
DB_HOST=
DB_USER=
DB_PASS=
```
3/4. Переходим в рабочий каталог:
```
cd menu/
```
4. Создаем файл миграции:
```
alembic revision --autogenerate -m "You're comment here"
```
5. Запускаем миграции:
```
alembic upgrade head
```
6. Запускаем проект
```
uvicorn main:menu_app --reload
```

## Тестируем

Через Postman с помощью файлов из папки tests


Так же ознакомится с функционалом можно через SWAGGER
```
http://127.0.0.1:8000/docs
```