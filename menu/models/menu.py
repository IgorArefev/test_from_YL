from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from menu.models.base import Base

if TYPE_CHECKING:
    from menu.models.submenu import SubMenu


class Menu(Base):
    """Модель меню."""
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    submenu: Mapped[list['SubMenu']] = relationship('SubMenu', cascade='delete')
