from httpx import AsyncClient

from menu.schemas.menu import MenuResponse
from menu.schemas.submenu import SubmenuResponse
from menu.schemas.dish import DishResponse
from menu.api.routers import MENU_PREFIX


async def test_create_dish(
        async_client: AsyncClient,
        test_menu: MenuResponse,
        test_submenu: SubmenuResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/"
    body = {
        "title": "My dish 1",
        "description": "My dish description 1",
        "price": "12.50",
    }
    response = await async_client.post(url, json=body)
    assert response.status_code == 201
    assert response.json()["title"] == "My dish 1"
    assert response.json()["description"] == "My dish description 1"
    assert response.json()["price"] == "12.50"


async def test_get_one_dish(
        async_client: AsyncClient,
        test_menu: MenuResponse,
        test_submenu: SubmenuResponse,
        test_dish: DishResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/{test_dish.id}"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json()["title"] == test_submenu.title
    assert response.json()["description"] == test_submenu.description
    assert response.json()["price"] == test_submenu.description


async def test_get_all_dishes(
    async_client: AsyncClient,
    test_menu: MenuResponse,
    test_submenu: SubmenuResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_update_dish(
    async_client: AsyncClient,
    test_menu: MenuResponse,
    test_submenu: SubmenuResponse,
    test_dish: DishResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/{test_dish.id}"
    body = {
        "title": "My updated dish 1",
        "description": "My updated dish description 1",
        "price": "14.50",
    }
    response = await async_client.patch(url, json=body)
    assert response.status_code == 200
    assert response.json()["title"] == "My updated dish 1"
    assert response.json()["description"] == "My updated dish description 1"
    assert response.json()["price"] == "14.50"


async def test_delete_dish(
    async_client: AsyncClient,
    test_menu: MenuResponse,
    test_submenu: SubmenuResponse,
    test_dish: DishResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}/dishes/{test_dish.id}"
    response = await async_client.delete(url)
    assert response.status_code == 200
