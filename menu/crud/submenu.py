from sqlalchemy import func, select

from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models import Dish
from menu.models.submenu import SubMenu

submenu_crud = CRUDBase(SubMenu)
submenu_validators = Validators(SubMenu)


async def dishes_counter(_id, session):
    """Подсчет блюд в подменю"""
    querry = (
        select(
            func.count(Dish.id)
        )
        .where(Dish.submenu_id == _id)
    )
    result = await session.scalars(querry)
    return result.first()
