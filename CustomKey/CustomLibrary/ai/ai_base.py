from ..baseclass import BaseHandler


class AiBaseHandler(BaseHandler):
    """
    AI智能降噪测试
    """

    @property
    def has_license(self):
        cache_k = 'has_license'
        cache_v = self.cache.get(cache_k)
        if cache_v is not None:
            return cache_v

        url = self.make_url('/maxs/pm/system/license/queryLic.do')
        res = self.session.get(url).json()
        ai_license = list(filter(lambda x: x['featureCode'] == 'N5G4', res['data']))

        result = False
        if ai_license and ai_license[0]['licStatus'] == 'effective':
            result = True

        self.cache.update({cache_k: result})
        return result
