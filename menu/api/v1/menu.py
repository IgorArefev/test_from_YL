from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.menu import menu_crud, menu_validators
from menu.schemas.menu import MenuCreate, MenuGet, MenuUpdate


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_menu(
    menu: MenuCreate, session: AsyncSession = Depends(get_async_session)
):
    await menu_validators.uniq_name_check(menu.title, session)
    return await menu_crud.create(menu, session)


@router.get(
    "/{target_menu_id}",
    response_model=MenuGet,
    status_code=status.HTTP_200_OK
)
async def get_menu(
    target_menu_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    if not await menu_validators.id_object_exist(target_menu_id, session):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="menu not found"
        )
    item = await menu_crud.get_one_by_id(target_menu_id, session)
    item = jsonable_encoder(item)
    item["submenus_count"] = await menu_crud.submenus_counter(
        target_menu_id,
        session
    )
    item["dishes_count"] = await menu_crud.dishes_counter(
        target_menu_id,
        session
    )
    return item


@router.get("/", status_code=status.HTTP_200_OK)
async def get_menus(session: AsyncSession = Depends(get_async_session)):
    return await menu_crud.get_all_from_model(session)


@router.patch("/{target_menu_id}", status_code=status.HTTP_200_OK)
async def update_menu_value(
    target_menu_id: UUID4,
    new_value: MenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    target_menu = await menu_crud.get_one_by_id(target_menu_id, session)
    await menu_validators.uniq_name_check(new_value.title, session)
    return await menu_crud.update(target_menu, new_value, session)


@router.delete("/{target_menu_id}", status_code=status.HTTP_200_OK)
async def delete_target_menu(
    target_menu_id: UUID4, session: AsyncSession = Depends(get_async_session)
):
    target_menu = await menu_crud.get_one_by_id(target_menu_id, session)
    return await menu_crud.delete(target_menu, session)
