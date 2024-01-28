from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models.dish import Dish

dish_crud = CRUDBase(Dish)
dish_validators = Validators(Dish)
