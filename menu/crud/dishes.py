from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models.dishes import Dishes

dish_crud = CRUDBase(Dishes)
dish_validators = Validators(Dishes)
