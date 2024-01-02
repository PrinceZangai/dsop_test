from .ai_base import AiBaseHandler
from ..base import no_license_pass, pass_unittest


class AiViewHandler(AiBaseHandler):
    """
    AI降噪-总览
    """
    time_range = ['30m', '1h', '7d', '30d', '90d']

    @pass_unittest()
    @no_license_pass(True)
    def test_top5(self):
        url = self.make_url(f'/maxs/sdb/overview/getModelTop5')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, msg: {res["message"]}'

        return True

    @pass_unittest()
    @no_license_pass(True)
    def test_status(self):
        url = self.make_url(f'/maxs/sdb/overview/getModelStatus')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, msg: {res["message"]}'

        return True

    @pass_unittest()
    @no_license_pass(True)
    def test_statistic(self):
        for duration in self.time_range:
            url = self.make_url(f'/maxs/sdb/overview/getEsCache/{duration}')
            res = self.session.get(url).json()
            assert res['code'] == 200, f'接口出错，url：{url}, msg: {res["message"]}'

        return True
