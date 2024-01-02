from .mine import MineHandler
from ..baseclass import BaseProxy


class MineProxy(BaseProxy):

    def get_mine_handler(self, *args, **kwargs):
        return self.get_handler(MineHandler, *args, **kwargs)
