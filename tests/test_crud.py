from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from menu.core.config import settings
from menu.core.db import engine
from menu.models.base import Base
from menu.schemas.dish import DishResponse
from menu.schemas.menu import MenuResponse
from menu.schemas.submenu import SubmenuResponse


@pytest.fixture(autouse=True)
async def clear_db() -> None:
    async with engine.begin() as connection:
        assert settings.mode == 'TEST_LOCAL' or settings.mode == 'TEST_DEV'
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)


class TestGetOne:

    async def test_get_menu(
            self,
            async_client: AsyncClient,
            default_menu: MenuResponse,
            menu_url: str
    ) -> None:
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == str(default_menu.id)
        assert response.json()['title'] == default_menu.title
        assert response.json()['description'] == default_menu.description

    async def test_get_submenu(
            self,
            async_client: AsyncClient,
            default_submenu: SubmenuResponse,
            submenu_url: str
    ) -> None:
        response = await async_client.get(submenu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == str(default_submenu.id)
        assert response.json()['title'] == default_submenu.title
        assert response.json()['description'] == default_submenu.description

    async def test_get_dish(
            self,
            async_client: AsyncClient,
            default_dish: DishResponse,
            dish_url: str
    ) -> None:
        response = await async_client.get(dish_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == str(default_dish.id)
        assert response.json()['title'] == default_dish.title
        assert response.json()['description'] == default_dish.description

    async def test_get_one_not_found(
            self,
            async_client: AsyncClient,
            menus_url: str,
            submenus_url: str,
            dishes_url: str
    ) -> None:
        uuid = str(uuid4())
        response = await async_client.get(menus_url + uuid)
        assert response.json()['detail'] == 'menu not found'
        response = await async_client.get(submenus_url + uuid)
        assert response.json()['detail'] == 'submenu not found'
        response = await async_client.get(dishes_url + uuid)
        assert response.json()['detail'] == 'dish not found'


class TestGetAll:

    async def test_get_menus(
            self,
            async_client: AsyncClient,
            default_menu: MenuResponse,
            menus_url: str
    ) -> None:
        response = await async_client.get(menus_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []

    async def test_get_submenus(
            self,
            async_client: AsyncClient,
            default_submenu: SubmenuResponse,
            submenus_url: str
    ) -> None:
        response = await async_client.get(submenus_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []

    async def test_get_dishes(
            self,
            async_client: AsyncClient,
            default_dish: DishResponse,
            dishes_url: str
    ) -> None:
        response = await async_client.get(dishes_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() != []


class TestPost:

    async def test_create_menu(
            self,
            async_client: AsyncClient,
            menus_url
    ) -> None:
        body = {
            'title': 'My menu 1',
            'description': 'My menu description 1',
        }
        response = await async_client.get(menus_url)
        assert response.json() == []
        new_menu = await async_client.post(menus_url, json=body)
        assert new_menu.status_code == status.HTTP_201_CREATED
        response = await async_client.get(menus_url)
        assert response.json()[0]['id'] == new_menu.json()['id']
        assert response.json()[0]['title'] == new_menu.json()['title']
        assert response.json()[0]['description'] == new_menu.json()['description']
        new_menu = await async_client.post(menus_url, json=body)
        assert new_menu.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert new_menu.json()['detail'] == 'already exist'

    async def test_create_submenu(
            self,
            async_client: AsyncClient,
            submenus_url: str
    ) -> None:
        body = {
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
        }
        response = await async_client.get(submenus_url)
        assert response.json() == []
        new_submenu = await async_client.post(submenus_url, json=body)
        assert new_submenu.status_code == status.HTTP_201_CREATED
        response = await async_client.get(submenus_url)
        assert response.json()[0]['id'] == new_submenu.json()['id']
        assert response.json()[0]['title'] == new_submenu.json()['title']
        assert response.json()[0]['description'] == new_submenu.json()['description']
        new_submenu = await async_client.post(submenus_url, json=body)
        assert new_submenu.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert new_submenu.json()['detail'] == 'already exist'

    async def test_create_dish(
            self,
            async_client: AsyncClient,
            dishes_url: str
    ) -> None:
        body = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
        }
        response = await async_client.get(dishes_url)
        assert response.json() == []
        new_dish = await async_client.post(dishes_url, json=body)
        assert new_dish.status_code == status.HTTP_201_CREATED
        response = await async_client.get(dishes_url)
        assert response.json()[0]['id'] == new_dish.json()['id']
        assert response.json()[0]['title'] == new_dish.json()['title']
        assert response.json()[0]['description'] == new_dish.json()['description']
        assert response.json()[0]['price'] == new_dish.json()['price']
        new_dish = await async_client.post(dishes_url, json=body)
        assert new_dish.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert new_dish.json()['detail'] == 'already exist'


class TestPatch:

    async def test_update_menu(
            self,
            async_client: AsyncClient,
            menu_url: str
    ) -> None:
        body = {
            'title': 'My updated menu 1',
            'description': 'My updated menu description 1',
        }
        response = await async_client.get(menu_url)
        assert response.json()['title'] != body['title']
        assert response.json()['description'] != body['description']
        updated_munu = await async_client.patch(menu_url, json=body)
        assert updated_munu.status_code == status.HTTP_200_OK
        response = await async_client.get(menu_url)
        assert response.json()['title'] == body['title']
        assert response.json()['description'] == body['description']
        updated_munu = await async_client.patch(menu_url, json=body)
        assert updated_munu.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert updated_munu.json()['detail'] == 'already exist'

    async def test_update_submenu(
            self,
            async_client: AsyncClient,
            submenu_url: str
    ) -> None:
        body = {
            'title': 'My updated submenu 1',
            'description': 'My updated submenu description 1',
        }
        response = await async_client.get(submenu_url)
        assert response.json()['title'] != body['title']
        assert response.json()['description'] != body['description']
        updated_submenu = await async_client.patch(submenu_url, json=body)
        assert updated_submenu.status_code == status.HTTP_200_OK
        response = await async_client.get(submenu_url)
        assert response.json()['title'] == body['title']
        assert response.json()['description'] == body['description']
        updated_submenu = await async_client.patch(submenu_url, json=body)
        assert updated_submenu.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert updated_submenu.json()['detail'] == 'already exist'

    async def test_update_dish(
        self,
        async_client: AsyncClient,
        dish_url: str
    ) -> None:
        body = {
            'title': 'My updated dish 1',
            'description': 'My updated dish description 1',
            'price': '14.50',
        }
        response = await async_client.get(dish_url)
        assert response.json()['title'] != body['title']
        assert response.json()['description'] != body['description']
        assert response.json()['price'] != body['price']
        updated_dish = await async_client.patch(dish_url, json=body)
        assert updated_dish.status_code == status.HTTP_200_OK
        response = await async_client.get(dish_url)
        assert response.json()['title'] == body['title']
        assert response.json()['description'] == body['description']
        assert response.json()['price'] == body['price']
        updated_dish = await async_client.patch(dish_url, json=body)
        assert updated_dish.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert updated_dish.json()['detail'] == 'already exist'


class TestDelete:

    async def test_delete_menu(
            self,
            async_client: AsyncClient,
            menu_url: str
    ) -> None:
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_200_OK
        deleted_menu = await async_client.delete(menu_url)
        assert deleted_menu.status_code == status.HTTP_200_OK
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'menu not found'

    async def test_delete_submenu(
        self,
        async_client: AsyncClient,
        submenu_url: str
    ) -> None:
        response = await async_client.get(submenu_url)
        assert response.status_code == status.HTTP_200_OK
        deleted_submenu = await async_client.delete(submenu_url)
        assert deleted_submenu.status_code == status.HTTP_200_OK
        response = await async_client.get(submenu_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'submenu not found'

    async def test_delete_dish(
        self,
        async_client: AsyncClient,
        dish_url: str
    ) -> None:
        response = await async_client.get(dish_url)
        assert response.status_code == status.HTTP_200_OK
        deleted_dish = await async_client.delete(dish_url)
        assert deleted_dish.status_code == status.HTTP_200_OK
        response = await async_client.get(dish_url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()['detail'] == 'dish not found'
