from .monitor import MoniHandler
from ..baseclass import BaseProxy


class MoniProxy(BaseProxy):

    def get_moni_handler(self, *args, **kwargs):
        return self.get_handler(MoniHandler, *args, **kwargs)
