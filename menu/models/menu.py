from sqlalchemy import Column, Text
from sqlalchemy.orm import relationship

from menu.core.db import Base


class Menus(Base):
    title = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    submenu = relationship("SubMenus", cascade="delete")
