from fastapi import APIRouter

from menu.api.v1 import dish_router, menu_router, submenu_router

main_router = APIRouter()

main_router.include_router(
    menu_router,
    prefix="/api/v1/menus",
    tags=["Menus"]
)
main_router.include_router(
    submenu_router,
    prefix="/api/v1/menus/{target_menu_id}/submenus", tags=["Submenus"]
)
main_router.include_router(
    dish_router,
    prefix=(
        "/api/v1/menus/{target_menu_id}/submenus/{target_submenu_id}/dishes"
    ),
    tags=["Dishes"],
)
