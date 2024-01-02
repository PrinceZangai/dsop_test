from .alarm import AlarmHandler
from .pre_alarm import PreAlarmHandler
from ..baseclass import BaseProxy


class AlarmProxy(BaseProxy):

    def get_alarm_handler(self, *args, **kwargs):
        return self.get_handler(AlarmHandler, *args, **kwargs)

    def get_pre_alarm_handler(self, *args, **kwargs):
        return self.get_handler(PreAlarmHandler, *args, **kwargs)
