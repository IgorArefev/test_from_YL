from pydantic import BaseModel, UUID4


class DishesBase(BaseModel):
    title: str
    description: str
    price: str


class DishesCreate(DishesBase):
    pass


class DishesUpdate(DishesBase):
    pass


class DishResponse(DishesBase):
    id: UUID4
    submenu_id: UUID4
