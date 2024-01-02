from .order import OrderManage
from ..baseclass import BaseProxy


class OrderManageProxy(BaseProxy):

    def get_om_handler(self, *args, **kwargs):
        return self.get_handler(OrderManage, *args, **kwargs)
