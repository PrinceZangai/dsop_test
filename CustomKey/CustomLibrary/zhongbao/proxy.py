from .protect import ProtectHandler
from ..baseclass import BaseProxy


class ProtectProxy(BaseProxy):

    def get_protect_handler(self, *args, **kwargs):
        return self.get_handler(ProtectHandler, *args, **kwargs)
