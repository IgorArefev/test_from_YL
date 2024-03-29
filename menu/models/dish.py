from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from menu.models.base import Base


class Dish(Base):
    """Модель блюд."""
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[str] = mapped_column(nullable=False)
    submenu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('submenu.id'))
