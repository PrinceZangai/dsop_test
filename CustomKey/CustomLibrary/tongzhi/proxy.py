from .notify import NotifyHandler
from ..baseclass import BaseProxy


class NotifyProxy(BaseProxy):

    def get_notify_handler(self, *args, **kwargs):
        return self.get_handler(NotifyHandler, *args, **kwargs)
