from .ai_config import AiCfgHandler
from .ai_event import AiEventHandler
from .ai_model import AiModelHandler
from .ai_view import AiViewHandler
from .ai_warn import AiWarnHandler

handler_cache = dict()


class AiProxy:

    def get_handler(self, cls, *args, **kwargs):
        if handler_cache.get(cls.__name__) is None:
            ins = cls(*args, **kwargs)
            handler_cache.update({cls.__name__: ins})

        return handler_cache.get(cls.__name__)

    def get_ai_cfg_handler(self, *args, **kwargs):
        return self.get_handler(AiCfgHandler, *args, **kwargs)

    def get_ai_warn_handler(self, *args, **kwargs):
        return self.get_handler(AiWarnHandler, *args, **kwargs)

    def get_ai_event_handler(self, *args, **kwargs):
        return self.get_handler(AiEventHandler, *args, **kwargs)

    def get_ai_view_handler(self, *args, **kwargs):
        return self.get_handler(AiViewHandler, *args, **kwargs)

    def get_ai_model_handler(self, *args, **kwargs):
        return self.get_handler(AiModelHandler, *args, **kwargs)
