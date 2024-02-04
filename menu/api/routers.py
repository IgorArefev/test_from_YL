from fastapi import APIRouter

from menu.api.v1 import dish_router, menu_router, submenu_router

main_router = APIRouter()

MENU_PREFIX = '/api/v1/menus'
SUBMENU_PREFIX = '/api/v1/menus/{target_menu_id}/submenus'
DISH_PREFIX = (
    '/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes'
)

main_router.include_router(
    menu_router,
    prefix=MENU_PREFIX,
    tags=['Menus']
)
main_router.include_router(
    submenu_router,
    prefix=SUBMENU_PREFIX,
    tags=['Submenus']
)
main_router.include_router(
    dish_router,
    prefix=DISH_PREFIX,
    tags=['Dishes'],
)
