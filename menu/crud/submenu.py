from menu.api.v1.validators import Validators
from menu.crud.base import CRUDBase
from menu.models.submenu import SubMenus

submenu_crud = CRUDBase(SubMenus)
submenu_validators = Validators(SubMenus)
