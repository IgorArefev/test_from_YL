from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.submenu import dishes_counter, submenu_crud, submenu_validators
from menu.schemas.submenu import SubMenuCreate, SubMenuUpdate

router = APIRouter()
DETAIL = 'submenu not found'


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def create_new_submenu(
    target_menu_id: UUID4,
    menu: SubMenuCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создает новое подменю."""

    await submenu_validators.uniq_name_check(menu.title, session)
    return await submenu_crud.create(menu, session, target_menu_id)


@router.get(
    '/{target_submenu_id}',
    status_code=status.HTTP_200_OK
)
async def get_submenu(
    target_submenu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    """Получает подменю по id."""
    await submenu_validators.id_object_exist(
        target_submenu_id,
        session,
        DETAIL
    )
    item = await submenu_crud.get_one_by_id(
        target_submenu_id,
        session
    )
    item = jsonable_encoder(item)
    item['dishes_count'] = await dishes_counter(
        target_submenu_id,
        session
    )
    return item


@router.get(
    '/',
    status_code=status.HTTP_200_OK
)
async def get_submenus(
        session: AsyncSession = Depends(get_async_session)
):
    """Получает все подменю."""

    return await submenu_crud.get_all(session)


@router.patch(
    '/{target_submenu_id}',
    status_code=status.HTTP_200_OK
)
async def update_submenu_value(
    target_submenu_id: UUID4,
    new_value: SubMenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновляет поля у подменю."""

    await submenu_validators.id_object_exist(
        target_submenu_id,
        session,
        DETAIL
    )
    target_menu = await submenu_crud.get_one_by_id(
        target_submenu_id,
        session
    )
    await submenu_validators.uniq_name_check(
        new_value.title,
        session
    )
    return await submenu_crud.update(
        target_menu,
        new_value,
        session
    )


@router.delete(
    '/{target_submenu_id}',
    status_code=status.HTTP_200_OK
)
async def delete_target_submenu(
    target_submenu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    """Удаляет подменю."""

    await submenu_validators.id_object_exist(
        target_submenu_id,
        session,
        DETAIL
    )
    target_menu = await submenu_crud.get_one_by_id(
        target_submenu_id,
        session
    )
    return await submenu_crud.delete(target_menu, session)
