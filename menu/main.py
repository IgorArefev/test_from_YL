from fastapi import FastAPI

from menu.api.routers import main_router
from menu.core.config import settings

menu_app = FastAPI(title=settings.app_name, description=settings.description)

menu_app.include_router(main_router)
