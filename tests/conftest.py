import asyncio

import pytest
from httpx import AsyncClient

from menu.api.routers import MENU_PREFIX
from menu.core.config import settings
from menu.core.db import engine
from menu.main import menu_app
from menu.models.base import Base
from menu.schemas.dish import DishResponse
from menu.schemas.menu import MenuResponse
from menu.schemas.submenu import SubmenuResponse

BASE_URL = 'http://localhost'


@pytest.fixture(scope='session', autouse=True)
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session', autouse=True)
async def clear_db() -> None:
    async with engine.begin() as connection:
        assert settings.mode == 'TEST_LOCAL' or settings.mode == 'TEST_DEV'
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture()
async def async_client() -> AsyncClient:
    async with AsyncClient(app=menu_app, base_url=BASE_URL) as client:
        yield client
        await client.aclose()


@pytest.fixture()
async def default_menu(
        async_client: AsyncClient,
        menus_url: str
) -> MenuResponse:
    return MenuResponse.model_validate(
        (
            await async_client.post(
                menus_url,
                json={
                    'title': 'My menu 1',
                    'description': 'My menu description 1',
                },
            )
        ).json(),
    )


@pytest.fixture()
async def default_submenu(
        async_client: AsyncClient,
        default_menu: MenuResponse,
        submenus_url: str
) -> SubmenuResponse:
    return SubmenuResponse.model_validate(
        (
            await async_client.post(
                submenus_url,
                json={
                    'title': 'My submenu 1',
                    'description': 'My submenu description 1',
                },
            )
        ).json(),
    )


@pytest.fixture()
async def default_dish(
        async_client: AsyncClient,
        default_menu: MenuResponse,
        default_submenu: SubmenuResponse,
        dishes_url: str
) -> DishResponse:
    return DishResponse.model_validate(
        (
            await async_client.post(
                dishes_url,
                json={
                    'title': 'My dish 1',
                    'description': 'My dish description 1',
                    'price': '12.50',
                },
            )
        ).json(),
    )


@pytest.fixture()
def menus_url() -> str:
    url = (
        f'{MENU_PREFIX}/'
    )
    return url


@pytest.fixture()
def menu_url(
        default_menu: MenuResponse
) -> str:
    url = (
        f'{MENU_PREFIX}/'
        f'{default_menu.id}'
    )
    return url


@pytest.fixture()
def submenus_url(
        default_menu: MenuResponse
) -> str:
    url = (
        f'{MENU_PREFIX}/'
        f'{default_menu.id}/'
        'submenus/'
    )
    return url


@pytest.fixture()
def submenu_url(
        default_menu: MenuResponse,
        default_submenu: SubmenuResponse
) -> str:
    url = (
        f'{MENU_PREFIX}/'
        f'{default_menu.id}/'
        'submenus/'
        f'{default_submenu.id}'
    )
    return url


@pytest.fixture()
def dishes_url(
        default_menu: MenuResponse,
        default_submenu: SubmenuResponse
) -> str:
    url = (
        f'{MENU_PREFIX}/'
        f'{default_menu.id}/'
        'submenus/'
        f'{default_submenu.id}/'
        'dishes/'
    )
    return url


@pytest.fixture()
def dish_url(
        default_menu: MenuResponse,
        default_submenu: SubmenuResponse,
        default_dish: DishResponse
) -> str:
    url = (
        f'{MENU_PREFIX}/'
        f'{default_menu.id}/'
        'submenus/'
        f'{default_submenu.id}/'
        'dishes/'
        f'{default_dish.id}'
    )
    return url
