from typing import Type

from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from menu.core.db import AsyncSessionLocal, Base


class Validators:
    """Дополнительные методы валидации."""

    def __init__(self, model: Type[Base]) -> None:
        self.model = model

    async def uniq_name_check(
            self,
            name: str,
            session: AsyncSessionLocal
    ) -> None:
        """Проверка поля на уникальность."""

        duplicate = await session.execute(
            select(self.model)
            .where(self.model.title == name)
        )
        duplicate = duplicate.scalars().first()
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="already exist"
            )

    async def id_object_exist(
            self,
            _id: UUID4,
            session: AsyncSessionLocal
    ) -> Type[Base] | None:
        """Проверка существует ли модель."""

        item = await session.execute(
            select(self.model)
            .where(self.model.id == _id))
        return item.scalars().first()
