from sqlalchemy import Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID

from menu.core.db import Base


class Dishes(Base):
    title = Column(Text, nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Text, nullable=False)
    submenu_id = Column(UUID(as_uuid=True), ForeignKey("submenus.id"))
