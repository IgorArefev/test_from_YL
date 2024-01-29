from httpx import AsyncClient

from menu.schemas.menu import MenuResponse
from menu.api.routers import MENU_PREFIX


async def test_create_menu(
        async_client: AsyncClient
):
    url = f"{MENU_PREFIX}/"
    body = {
        "title": "My menu 1",
        "description": "My menu description 1",
    }
    response = await async_client.post(url, json=body)
    assert response.status_code == 201
    assert response.json()["title"] == "My menu 1"
    assert response.json()["description"] == "My menu description 1"


async def test_get_one_menu(
        async_client: AsyncClient,
        test_menu: MenuResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}/"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json()["title"] == test_menu.title
    assert response.json()["description"] == test_menu.description


async def test_get_all_menus(
        async_client: AsyncClient
):
    url = f"{MENU_PREFIX}/"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_update_menu(
        async_client: AsyncClient,
        test_menu: MenuResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}"
    body = {
        "title": "My updated menu 1",
        "description": "My updated menu description 1",
    }
    response = await async_client.patch(url, json=body)
    assert response.status_code == 200
    assert response.json()["title"] == "My updated menu 1"
    assert response.json()["description"] == "My updated menu description 1"


async def test_delete_menu(
        async_client: AsyncClient,
        test_menu: MenuResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}"
    response = await async_client.delete(url)
    assert response.status_code == 200
    new_response = await async_client.get(url)
    assert new_response.status_code == 404
