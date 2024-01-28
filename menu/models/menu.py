from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship, Mapped, mapped_column

from menu.core.db import Base

if TYPE_CHECKING:
    from menu.models.submenu import SubMenu


class Menu(Base):
    """Модель меню."""
    title: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=False)
    submenu: Mapped[list["SubMenu"]] = relationship("SubMenu", cascade="delete")
