from .bi import BiHandler
from ..baseclass import BaseProxy


class BiProxy(BaseProxy):

    def get_bi_handler(self, *args, **kwargs):
        return self.get_handler(BiHandler, *args, **kwargs)
