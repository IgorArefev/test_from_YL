from sqlalchemy import select
from sqlalchemy.orm import joinedload

from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models.menu import Menu
from menu.models.submenu import SubMenu

menu_crud = CRUDBase(Menu)
menu_validators = Validators(Menu)


async def counter(_id, session):
    """
    Запрос на получение всех подменю
    и блюд у запрашиваемого меню.
    """

    querry = (
        select(SubMenu)
        .options(joinedload(SubMenu.dish))
        .where(SubMenu.menu_id == _id)
        .order_by(SubMenu.id)
    )
    result = await session.scalars(querry)
    return result.unique().all()
