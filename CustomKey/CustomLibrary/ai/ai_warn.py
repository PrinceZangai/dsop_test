import os
import time

from .ai_base import AiBaseHandler
from ..base import get_ctime_str, get_time_days_ago, get_now
from ..base import no_license_pass, pass_unittest
from ..connector import SocketConnector


class AiWarnHandler(AiBaseHandler):
    """
    AI降噪-告警
    """

    def __init__(self, domain, cookies, master=None):
        super().__init__(domain, cookies, master)
        self.make_ai_warns()

    @pass_unittest()
    @no_license_pass()
    def make_ai_warns(self):
        # 开启降噪
        url = self.make_url('/maxs/sdb/cfg/setCfg')
        data = {"evolution": 1, "evolutionCondition": 0, "handleDuration": 10, "label": 1,
                "sampleTriggerNumber": 20000,
                "sdb": 1, "strategy": 1, "strategyType": 1, "score": 0.5}
        self.session.post(url, json=data).json()

        # 发送日志
        log_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'Web服务器遭受大规模网络攻击', 'tda.log')
        conn = SocketConnector(self.master, port=8805)
        for _ in range(1000):
            conn.send_log(log_file, False)

        conn.close()

        # 轮训等待告警产生
        for _ in range(300):
            res = self.get_warns()
            warns = res['data']['rowData']
            if warns:
                break

            time.sleep(10)
        else:
            raise Exception("此环境5分钟内未产生AI标记的告警")

    def get_warns(self, page=1, page_size=10, start=None, end=None, tag='全部') -> dict:
        """获取告警列表"""
        url = self.make_url('/maxs/rv/alarm/pageAlarm')
        end_time = end or get_ctime_str()
        now = get_now()
        start_time = start or get_time_days_ago(now, 7)
        payload = {
            "pageIndex": page,
            "pageSize": page_size,
            "startTime": start_time,
            "endTime": end_time,
            "aiTags": tag
        }

        res = self.session.post(url=url, json=payload)
        j_res = res.json()
        return j_res

    @pass_unittest()
    @no_license_pass(True)
    def test_ai_filter(self):
        """安全告警-智能降噪-AI辅助研判复选框过滤"""
        res = self.get_warns()
        assert res['code'] == 200, 'AI辅助研判-告警列表，接口出错'

        records = res.get('data', {}).get('rowData', [])
        if records:
            record = records[0]
            fields = list(record.keys())
            assert 'AI_SCORE' in fields
            assert 'AI_TAG' in fields
            assert 'AI_MODEL' in fields

        return True

    @pass_unittest()
    @no_license_pass(True)
    def test_mark_warn(self):
        res = self.get_warns(page_size=10000)
        records = res.get('data', {}).get('rowData', [])
        warn_ids = [i['SNOW_ID'] for i in records]

        end_time = get_ctime_str()
        now = get_now()
        start_time = get_time_days_ago(now, 7)

        half = len(warn_ids) // 2

        mark_noise_ids = warn_ids[:half]
        mark_warn_ids = warn_ids[half:]

        payload_noise = {
            "startTime": start_time,
            "endTime": end_time,
            "aiTag": "噪声",
            "ids": mark_noise_ids
        }
        payload_warn = {
            "startTime": start_time,
            "endTime": end_time,
            "aiTag": '告警',
            "ids": mark_warn_ids
        }

        url = self.make_url('/maxs/rv/alarm/aiTag')
        res_noise = self.session.post(url=url, json=payload_noise).json()
        assert res_noise['code'] == 200, f'标注告警接口出错,msg:{res["message"]}'

        res_warn = self.session.post(url=url, json=payload_warn).json()
        assert res_warn['code'] == 200, f'标注告警接口出错,msg:{res["message"]}'

        return True
