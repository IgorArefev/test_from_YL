from typing import TYPE_CHECKING

from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from menu.models.base import Base

if TYPE_CHECKING:
    from menu.models.dish import Dish


class SubMenu(Base):
    """Модель подменю."""

    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    menu_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('menu.id'))
    dish: Mapped[list['Dish']] = relationship('Dish', cascade='delete')
