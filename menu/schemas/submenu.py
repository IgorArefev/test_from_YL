from pydantic import UUID4, BaseModel


class SubMenuBase(BaseModel):
    title: str
    description: str


class SubMenuGet(SubMenuBase):
    id: UUID4
    dishes_count: int


class SubMenuCreate(SubMenuBase):
    pass


class SubMenuUpdate(SubMenuBase):
    pass
