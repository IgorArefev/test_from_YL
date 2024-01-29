import asyncio

import pytest
from httpx import AsyncClient

from menu.core.db import Base, engine
from menu.main import menu_app
from menu.schemas.menu import MenuResponse
from menu.schemas.submenu import SubmenuResponse
from menu.schemas.dish import DishResponse
from menu.api.routers import MENU_PREFIX


@pytest.fixture(autouse=True)
async def db_clean():
    async with engine.begin() as async_engine:
        await async_engine.run_sync(Base.metadata.drop_all)
        await async_engine.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def async_client():
    async with AsyncClient(
            app=menu_app,
            base_url="http://localhost"
    ) as async_client:
        yield async_client


@pytest.fixture()
async def test_menu(
    async_client: AsyncClient
) -> MenuResponse:
    return MenuResponse.model_validate(
        (await async_client.post(MENU_PREFIX, json={
                                    "title": "My menu 1",
                                    "description": "My menu description 1",
                                },)).json(),
    )


@pytest.fixture()
async def test_submenu(
    async_client: AsyncClient,
    test_menu: MenuResponse,
) -> SubmenuResponse:
    return SubmenuResponse.model_validate(
        (await async_client.post(f"{MENU_PREFIX}/{test_menu.id}/submenus/",
                                 json={
                                     "title": "My submenu 1",
                                     "description": "My submenu description 1",
                                 },)).json(),
    )


@pytest.fixture()
async def test_dish(
    async_client: AsyncClient,
    test_menu: MenuResponse,
    test_submenu: SubmenuResponse,
) -> DishResponse:
    return DishResponse.model_validate(
        (await async_client.post(
                f"/{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/",
                json={
                    "title": "My dish 1",
                    "description": "My dish description 1",
                    "price": "12.50",
                },)).json(),
    )
