from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, select

from menu.models.dishes import Dishes
from menu.models.submenu import SubMenus


class CRUDBase:
    def __init__(self, model):
        self.model = model

    async def create(self, data, session, _id=None):
        new_data = data.model_dump()
        if self.model == SubMenus:
            new_data["menu_id"] = _id
        elif self.model == Dishes:
            new_data["submenu_id"] = _id
            new_data["price"] = str(round(float(new_data["price"]), 2))
        db_data = self.model(**new_data)
        session.add(db_data)
        await session.commit()
        await session.refresh(db_data)
        return db_data

    async def get_one_by_id(self, _id, session):
        item = await session.execute(
            select(self.model).where(self.model.id == _id)
        )
        return item.scalars().first()

    async def get_all_from_model(self, session):
        all_items = await session.execute(select(self.model))
        return all_items.scalars().all()

    async def update(self, current_value, new_value, session):
        old_data = jsonable_encoder(current_value)
        new_data = new_value.model_dump(exclude_unset=True)
        for field in old_data:
            if field in new_data:
                setattr(current_value, field, new_data[field])
        session.add(current_value)
        await session.commit()
        await session.refresh(current_value)
        return current_value

    async def delete(self, target, session):
        await session.delete(target)
        await session.commit()
        return target

    async def submenus_counter(self, _id, session):
        return await session.scalar(
            select(func.count(SubMenus.id))
            .where(SubMenus.menu_id == _id)
            .correlate_except(SubMenus)
        )

    async def dishes_counter(self, _id, session):
        return await session.scalar(
            select(func.count(Dishes.id))
            .where(
                Dishes.submenu_id.in_(
                    select(SubMenus.id).where(SubMenus.menu_id == _id)
                )
            )
            .correlate_except(Dishes)
        )

    async def submenu_dishes_counter(self, _id, session):
        return await session.scalar(
            select(func.count(Dishes.id))
            .where(Dishes.submenu_id == _id)
            .correlate_except(Dishes)
        )
