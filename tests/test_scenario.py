from collections import defaultdict

from fastapi import status
from httpx import AsyncClient

id_list = {}
counter: dict = defaultdict(int)


class TestScenario:

    async def test_create_new_menu(
            self,
            async_client: AsyncClient
    ) -> None:
        url = '/api/v1/menus/'
        body = {
            'title': 'My menu 1',
            'description': 'My menu description 1',
        }
        new_menu = await async_client.post(url, json=body)
        assert new_menu.status_code == status.HTTP_201_CREATED
        response = await async_client.get(url)
        assert response.json()[0]['id'] == new_menu.json()['id']
        id_list['menu_id'] = new_menu.json()['id']

    async def test_create_new_submenu(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_url = f'/api/v1/menus/{menu_id}/submenus/'
        body = {
            'title': 'My submenu 1',
            'description': 'My submenu description 1',
        }
        new_submenu = await async_client.post(submenu_url, json=body)
        assert new_submenu.status_code == status.HTTP_201_CREATED
        response = await async_client.get(submenu_url)
        assert response.json()[0]['id'] == new_submenu.json()['id']
        id_list['submenu_id'] = new_submenu.json()['id']
        counter['submenus_count'] += 1

    async def test_create_first_dish(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_id = id_list['submenu_id']
        dish_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/'
        body = {
            'title': 'My dish 1',
            'description': 'My dish description 1',
            'price': '12.50',
        }
        new_dish = await async_client.post(dish_url, json=body)
        assert new_dish.status_code == status.HTTP_201_CREATED
        response = await async_client.get(dish_url)
        assert response.json()[0]['id'] == new_dish.json()['id']
        id_list['dish1_id'] = new_dish.json()['id']
        counter['dishes_count'] += 1

    async def test_create_second_dish(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_id = id_list['submenu_id']
        dish_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/'
        body = {
            'title': 'My dish 2',
            'description': 'My dish description 2',
            'price': '13.50',
        }
        new_dish = await async_client.post(dish_url, json=body)
        assert new_dish.status_code == status.HTTP_201_CREATED
        response = await async_client.get(dish_url)
        assert response.json()[1]['id'] == new_dish.json()['id']
        id_list['dish2_id'] = new_dish.json()['id']
        counter['dishes_count'] += 1

    async def test_get_new_menu(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        menu_url = f'/api/v1/menus/{menu_id}'
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == id_list['menu_id']
        assert response.json()['submenus_count'] == counter['submenus_count']
        assert response.json()['dishes_count'] == counter['dishes_count']

    async def test_get_submenu(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_id = id_list['submenu_id']
        submenu_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        response = await async_client.get(submenu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == id_list['submenu_id']
        assert response.json()['dishes_count'] == counter['dishes_count']

    async def test_delete_submenu(
        self,
        async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_id = id_list['submenu_id']
        submenu_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}'
        deleted_submenu = await async_client.delete(submenu_url)
        assert deleted_submenu.status_code == status.HTTP_200_OK
        counter['submenus_count'] -= 1
        counter['dishes_count'] = 0

    async def test_get_submenus(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_url = f'/api/v1/menus/{menu_id}/submenus/'
        response = await async_client.get(submenu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    async def test_get_dishes(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_id = id_list['submenu_id']
        dish_url = f'/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes/'
        response = await async_client.get(dish_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    async def test_get_menu(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        menu_url = f'/api/v1/menus/{menu_id}'
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['id'] == id_list['menu_id']
        assert response.json()['submenus_count'] == counter['submenus_count']
        assert response.json()['dishes_count'] == counter['dishes_count']

    async def test_delete_menu(
        self,
        async_client: AsyncClient
    ) -> None:
        menu_id = id_list['menu_id']
        submenu_url = f'/api/v1/menus/{menu_id}'
        deleted_menu = await async_client.delete(submenu_url)
        assert deleted_menu.status_code == status.HTTP_200_OK
        counter['submenus_count'] = 0

    async def test_get_menus(
            self,
            async_client: AsyncClient
    ) -> None:
        menu_url = '/api/v1/menus/'
        response = await async_client.get(menu_url)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
