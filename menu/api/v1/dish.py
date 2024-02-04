from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.dish import dish_crud, dish_validators
from menu.schemas.dish import DishesCreate, DishesUpdate

router = APIRouter()
DETAIL = 'dish not found'


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED
)
async def create_new_dish(
    target_submenu_id: UUID4,
    menu: DishesCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await dish_validators.uniq_name_check(menu.title, session)
    return await dish_crud.create(menu, session, target_submenu_id)


@router.get(
    '/{target_dish_id}',
    status_code=status.HTTP_200_OK
)
async def get_dish(
    target_dish_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    return await dish_crud.get_one_by_id(
        target_dish_id,
        session,
        DETAIL
    )


@router.get(
    '/',
    status_code=status.HTTP_200_OK
)
async def get_dishes(
        session: AsyncSession = Depends(get_async_session)
):
    return await dish_crud.get_all(session)


@router.patch(
    '/{target_dish_id}',
    status_code=status.HTTP_200_OK
)
async def update_dish_value(
    target_dish_id: UUID4,
    new_value: DishesUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    target_menu = await dish_crud.get_one_by_id(
        target_dish_id,
        session,
        DETAIL
    )
    await dish_validators.uniq_name_check(new_value.title, session)
    return await dish_crud.update(target_menu, new_value, session)


@router.delete(
    '/{target_dish_id}',
    status_code=status.HTTP_200_OK
)
async def delete_target_dish(
    target_dish_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    target_menu = await dish_crud.get_one_by_id(
        target_dish_id,
        session,
        DETAIL
    )
    return await dish_crud.delete(target_menu, session)
