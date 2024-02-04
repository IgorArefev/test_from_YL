from pydantic import UUID4, BaseModel


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
