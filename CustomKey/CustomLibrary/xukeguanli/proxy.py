from .license import LicenseHandler
from ..baseclass import BaseProxy


class LicenseProxy(BaseProxy):

    def get_license_handler(self, *args, **kwargs):
        return self.get_handler(LicenseHandler, *args, **kwargs)
