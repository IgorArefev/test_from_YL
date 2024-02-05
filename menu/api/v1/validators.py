from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from menu.core.db import AsyncSessionLocal
from menu.models.base import Base


class Validators:
    """Дополнительные методы валидации."""

    def __init__(self, model: type[Base]):
        self.model = model

    async def uniq_name_check(
            self,
            name: str,
            session: AsyncSessionLocal
    ):
        """Проверка поля на уникальность."""

        duplicate = await session.execute(
            select(self.model)
            .where(self.model.title == name)
        )
        duplicate = duplicate.scalars().first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='already exist'
            )

    async def id_object_exist(
            self,
            _id: UUID4,
            session: AsyncSessionLocal,
            detail: str
    ):
        """Проверка существует ли модель."""

        item = await session.execute(
            select(self.model)
            .where(self.model.id == _id)
        )
        item = item.scalars().first()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )
