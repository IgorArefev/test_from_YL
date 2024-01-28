from typing import Any, Type

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy import UUID, select

from menu.api.v1.validators import Validators
from menu.core.db import AsyncSessionLocal, Base
from menu.models.dish import Dish
from menu.models.submenu import SubMenu


class CRUDBase:
    """Класс CRUD операций."""

    def __init__(self, model: Type[Base]) -> None:
        self.model = model

    async def create(
        self,
        data: Any,
        session: AsyncSessionLocal,
        _id: UUID = None
    ) -> Type[Base]:
        """Запись новой модели в базу."""

        new_data = data.model_dump()
        if self.model == SubMenu:
            new_data["menu_id"] = _id
        elif self.model == Dish:
            new_data["submenu_id"] = _id
            new_data["price"] = str(round(float(new_data["price"]), 2))
        db_data = self.model(**new_data)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)
        return db_data

    async def get_one_by_id(
        self,
        _id: UUID,
        session: AsyncSessionLocal,
        detail_text: str
    ) -> Type[Base]:
        """Выбор модели по id."""

        item = await Validators.id_object_exist(
            self,
            _id,
            session
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail_text
            )
        return item

    async def get_all(
        self,
        session: AsyncSessionLocal
    ) -> list[Type[Base]]:
        """Выбор всех моделей."""

        all_items = await session.execute(select(self.model))
        return all_items.scalars().all()

    async def update(
        self,
        current_value: Any,
        new_value: Any,
        session: AsyncSessionLocal
    ) -> Type[Base]:
        """Обновление модели."""

        old_data = jsonable_encoder(current_value)
        new_data = new_value.model_dump(exclude_unset=True)
        for field in old_data:
            if field in new_data:
                setattr(current_value, field, new_data[field])
        session.add(current_value)
        await session.commit()
        await session.refresh(current_value)
        return current_value

    async def delete(
        self,
        target: Type[Base],
        session: AsyncSessionLocal
    ) -> Type[Base]:
        """Удаление модели."""

        await session.delete(target)
        await session.commit()
        return target
