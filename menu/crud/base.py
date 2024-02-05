from typing import Any

from fastapi.encoders import jsonable_encoder
from sqlalchemy import UUID, select

from menu.core.db import AsyncSessionLocal
from menu.models.base import Base
from menu.models.dish import Dish
from menu.models.submenu import SubMenu


class CRUDBase:
    """Класс CRUD операций."""

    def __init__(self, model: type[Base]):
        self.model = model

    async def create(
        self,
        data: Any,
        session: AsyncSessionLocal,
        _id: UUID = None
    ):
        """Запись новой модели в базу."""

        new_data = data.model_dump()
        if self.model == SubMenu:
            new_data['menu_id'] = _id
        elif self.model == Dish:
            new_data['submenu_id'] = _id
            new_data['price'] = str(round(float(new_data['price']), 2))
        db_data = self.model(**new_data)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)
        return db_data

    async def get_one_by_id(
        self,
        _id: UUID,
        session: AsyncSessionLocal
    ):
        """Выбор модели по id."""

        item = await session.execute(
            select(self.model)
            .where(self.model.id == _id)
        )
        return item.scalars().first()

    async def get_all(
        self,
        session: AsyncSessionLocal
    ):
        """Выбор всех моделей."""

        all_items = await session.execute(select(self.model))
        return all_items.scalars().all()

    async def update(
        self,
        current_value: Any,
        new_value: Any,
        session: AsyncSessionLocal
    ):
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
        target: Any,
        session: AsyncSessionLocal
    ):
        """Удаление модели."""

        await session.delete(target)
        await session.commit()
        return target
