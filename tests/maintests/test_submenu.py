from httpx import AsyncClient

from menu.schemas.menu import MenuResponse
from menu.schemas.submenu import SubmenuResponse
from menu.api.routers import MENU_PREFIX


async def test_create_submenu(
        async_client: AsyncClient,
        test_menu: MenuResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/"
    body = {
        "title": "My submenu 1",
        "description": "My submenu description 1",
    }
    response = await async_client.post(url, json=body)
    assert response.status_code == 201
    assert response.json()["title"] == "My submenu 1"
    assert response.json()["description"] == "My submenu description 1"


async def test_get_one_submenu(
        async_client: AsyncClient,
        test_menu: MenuResponse,
        test_submenu: SubmenuResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json()["title"] == test_submenu.title
    assert response.json()["description"] == test_submenu.description


async def test_get_all_submenus(
        async_client: AsyncClient,
        test_menu: MenuResponse
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/"
    response = await async_client.get(url)
    assert response.status_code == 200
    assert response.json() == []


async def test_update_submenu(
        async_client: AsyncClient,
        test_menu: MenuResponse,
        test_submenu: SubmenuResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}"
    body = {
        "title": "My updated submenu 1",
        "description": "My updated submenu description 1",
    }
    response = await async_client.patch(url, json=body)
    assert response.status_code == 200
    assert response.json()["title"] == "My updated submenu 1"
    assert response.json()["description"] == "My updated submenu description 1"


async def test_delete_submenu(
        async_client: AsyncClient,
        test_menu: MenuResponse,
        test_submenu: SubmenuResponse,
):
    url = f"{MENU_PREFIX}/{test_menu.id}/submenus/{test_submenu.id}"
    response = await async_client.delete(url)
    assert response.status_code == 200
    new_response = await async_client.get(url)
    assert new_response.status_code == 404
