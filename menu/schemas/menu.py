from pydantic import UUID4, BaseModel


class MenuBase(BaseModel):
    title: str
    description: str


class MenuGet(MenuBase):
    id: UUID4
    submenus_count: int
    dishes_count: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass
