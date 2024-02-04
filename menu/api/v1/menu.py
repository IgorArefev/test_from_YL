from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.menu import counter, menu_crud, menu_validators
from menu.schemas.menu import MenuCreate, MenuGet, MenuUpdate

router = APIRouter()
DETAIL = 'menu not found'


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def create_new_menu(
    menu: MenuCreate,
    session: AsyncSession = Depends(get_async_session)
):
    await menu_validators.uniq_name_check(menu.title, session)
    return await menu_crud.create(menu, session)


@router.get(
    '/{target_menu_id}',
    response_model=MenuGet,
    status_code=status.HTTP_200_OK
)
async def get_menu(
    target_menu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    submenus_count = 0
    dishes_count = 0
    item = await menu_crud.get_one_by_id(
        target_menu_id,
        session,
        DETAIL
    )
    item = jsonable_encoder(item)
    count = await counter(target_menu_id, session)
    for value in count:
        if value.id:
            submenus_count += 1
        if value.dish:
            dishes_count += len(value.dish)
    item['submenus_count'] = submenus_count
    item['dishes_count'] = dishes_count
    return item


@router.get(
    '/',
    status_code=status.HTTP_200_OK
)
async def get_menus(
        session: AsyncSession = Depends(get_async_session)
):
    return await menu_crud.get_all(session)


@router.patch(
    '/{target_menu_id}',
    status_code=status.HTTP_200_OK
)
async def update_menu_value(
    target_menu_id: UUID4,
    new_value: MenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    target_menu = await menu_crud.get_one_by_id(
        target_menu_id,
        session,
        DETAIL
    )
    await menu_validators.uniq_name_check(new_value.title, session)
    return await menu_crud.update(target_menu, new_value, session)


@router.delete(
    '/{target_menu_id}',
    status_code=status.HTTP_200_OK
)
async def delete_target_menu(
    target_menu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    target_menu = await menu_crud.get_one_by_id(
        target_menu_id,
        session,
        DETAIL
    )
    return await menu_crud.delete(target_menu, session)
