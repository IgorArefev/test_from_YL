from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models.menu import Menus

menu_crud = CRUDBase(Menus)
menu_validators = Validators(Menus)
