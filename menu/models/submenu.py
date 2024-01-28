from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from menu.core.db import Base

if TYPE_CHECKING:
    from menu.models.dish import Dish
    from menu.models.menu import Menu


class SubMenu(Base):
    """Модель подменю."""

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    menu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("menu.id"))
    dish: Mapped[list["Dish"]] = relationship("Dish", cascade="delete")

