from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.dishes import dish_crud, dish_validators
from menu.schemas.dishes import DishesCreate, DishesUpdate


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_dish(
    target_submenu_id: UUID4,
    menu: DishesCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await dish_validators.uniq_name_check(menu.title, session)
    return await dish_crud.create(menu, session, target_submenu_id)


@router.get("/{target_dish_id}", status_code=status.HTTP_200_OK)
async def get_dish(
    target_dish_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    if not await dish_validators.id_object_exist(target_dish_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="dish not found"
        )
    return await dish_crud.get_one_by_id(target_dish_id, session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_dishes(session: AsyncSession = Depends(get_async_session)):
    return await dish_crud.get_all_from_model(session)


@router.patch("/{target_dish_id}", status_code=status.HTTP_200_OK)
async def update_dish_value(
    target_dish_id: UUID4,
    new_value: DishesUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    target_menu = await dish_crud.get_one_by_id(target_dish_id, session)
    await dish_validators.uniq_name_check(new_value.title, session)
    return await dish_crud.update(target_menu, new_value, session)


@router.delete("/{target_dish_id}", status_code=status.HTTP_200_OK)
async def delete_target_dish(
    target_dish_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    target_menu = await dish_crud.get_one_by_id(target_dish_id, session)
    return await dish_crud.delete(target_menu, session)
