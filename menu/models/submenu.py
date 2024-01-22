from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from menu.core.db import Base


class SubMenus(Base):
    title = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    menu_id = Column(UUID(as_uuid=True), ForeignKey("menus.id"))
    dish = relationship("Dishes", cascade="delete")
