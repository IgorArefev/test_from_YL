from pydantic import BaseModel


class DishesBase(BaseModel):
    title: str
    description: str
    price: str


class DishesCreate(DishesBase):
    pass


class DishesUpdate(DishesBase):
    pass
