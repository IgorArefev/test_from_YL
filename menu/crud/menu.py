from sqlalchemy import UUID, select
from sqlalchemy.orm import joinedload

from menu.api.v1.validators import Validators
from menu.core.db import AsyncSessionLocal
from menu.crud.base import CRUDBase
from menu.models.menu import Menu
from menu.models.submenu import SubMenu

menu_crud = CRUDBase(Menu)
menu_validators = Validators(Menu)


async def counter(_id: UUID, session: AsyncSessionLocal):
    """
    Запрос на получение всех подменю
    и блюд у запрашиваемого меню и их подсчет.
    """

    submenus_count = 0
    dishes_count = 0

    querry = (
        select(SubMenu)
        .options(joinedload(SubMenu.dish))
        .where(SubMenu.menu_id == _id)
        .order_by(SubMenu.id)
    )
    result = await session.scalars(querry)
    result = result.unique().all()
    for value in result:
        if value.id:
            submenus_count += 1
        if value.dish:
            dishes_count += len(value.dish)
    result = {
        'submenus_count': submenus_count,
        'dishes_count': dishes_count
    }
    return result
