from .collect import CollectHandler
from ..baseclass import BaseProxy


class CollectProxy(BaseProxy):

    def get_collect_handler(self, *args, **kwargs):
        return self.get_handler(CollectHandler, *args, **kwargs)
