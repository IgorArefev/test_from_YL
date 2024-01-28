from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from menu.core.db import Base
from menu.models.submenu import SubMenu


class Dish(Base):
    """Модель блюд."""
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    submenu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("submenu.id"))

