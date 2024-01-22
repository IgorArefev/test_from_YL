from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from menu.core.db import get_async_session
from menu.crud.submenu import submenu_crud, submenu_validators
from menu.schemas.submenu import SubMenuCreate, SubMenuUpdate

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_submenu(
    target_menu_id: UUID4,
    menu: SubMenuCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await submenu_validators.uniq_name_check(menu.title, session)
    return await submenu_crud.create(menu, session, target_menu_id)


@router.get("/{target_submenu_id}", status_code=status.HTTP_200_OK)
async def get_submenu(
    target_submenu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    if not await submenu_validators.id_object_exist(
            target_submenu_id,
            session
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="submenu not found"
        )
    item = await submenu_crud.get_one_by_id(target_submenu_id, session)
    item = jsonable_encoder(item)
    item["dishes_count"] = await submenu_crud.submenu_dishes_counter(
        target_submenu_id, session
    )
    return item


@router.get("/", status_code=status.HTTP_200_OK)
async def get_submenus(session: AsyncSession = Depends(get_async_session)):
    return await submenu_crud.get_all_from_model(session)


@router.patch("/{target_submenu_id}", status_code=status.HTTP_200_OK)
async def update_submenu_value(
    target_submenu_id: UUID4,
    new_value: SubMenuUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    target_menu = await submenu_crud.get_one_by_id(target_submenu_id, session)
    await submenu_validators.uniq_name_check(new_value.title, session)
    return await submenu_crud.update(target_menu, new_value, session)


@router.delete("/{target_submenu_id}", status_code=status.HTTP_200_OK)
async def delete_target_submenu(
    target_submenu_id: UUID4,
    session: AsyncSession = Depends(get_async_session)
):
    target_menu = await submenu_crud.get_one_by_id(target_submenu_id, session)
    return await submenu_crud.delete(target_menu, session)
