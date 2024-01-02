from ..base import get_time_ranges, TIME_FORMAT_1
from ..baseclass import BaseAlarmHandler


class AlarmHandler(BaseAlarmHandler):
    """
    工单管理
    """

    def prepare_data(self):
        # 发送日志
        self.make_warns()

    def test_exact_query(self):
        """1.安全告警普通搜索"""
        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {'handleStatus': '-1'}
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        alarm_name = res['data']['rowData'][0]['ALERT_NAME']

        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {'alertName': alarm_name, 'exact': '1', 'handleStatus': '-1'}
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def test_sort_query(self):
        """1.安全告警普通搜索"""
        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {'handleStatus': '-1', 'sort': 'RISK_LEVEL_DIC', 'order': 'asc'}
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {'handleStatus': '-1', 'sort': 'RISK_LEVEL_DIC', 'order': 'desc'}
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {'handleStatus': '-1', 'sort': 'COUNT', 'order': 'desc'}
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        count_list = [i['COUNT'] for i in res['data']['rowData']]
        count_copy = count_list.copy()
        count_list.sort(reverse=True)
        assert count_list == count_copy, f'攻击次数降序排序出错.res: {res}'

        return True

    def test_advanced_query(self):
        """高级搜索"""
        url = self.make_url(f'/maxs/rv/alarm/pageAlarm')
        query = {
            "advanced": 1,
            "conditionGroup": "{\"condition\":\"AND\",\"rowList\":[{\"operator\":\"equals\",\"key\":\"RISK_LEVEL\",\"value\":\"高危\"},{\"operator\":\"equals\",\"key\":\"RESULT\",\"value\":\"成功\"}],\"groupList\":[]}"
        }
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        query = {
            "advanced": 1,
            "conditionGroup": "{\"condition\":\"AND\",\"groupList\":[{\"condition\":\"AND\",\"rowList\":[{\"key\":\"HANDLE_STATUS\",\"operator\":\"equals\",\"value\":\"-1\"},{\"key\":\"HANDLE_DESC\",\"operator\":\"isExist\",\"value\":\"1\"}]}],\"rowList\":[{\"key\":\"ALERT_CAT_SECOND\",\"operator\":\"equals\",\"value\":\"Webshell攻击\"},{\"key\":\"ALERT_TEMPLATE\",\"operator\":\"equals\",\"value\":\"登录行为\"}]}"
        }
        res = self.get_warns(query=query)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def test_line_chart(self):
        """3.告警统计图-折线图"""
        url = self.make_url(f'/maxs/rv/alarm/alarmLineChar')
        time_range = get_time_ranges(TIME_FORMAT_1)
        start, end = time_range['最近7天']
        payload = {
            "pageIndex": 1,
            "pageSize": 10,
            "startTime": start,
            "endTime": end,
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_pie_chart(self):
        """4.告警统计图-处置状态"""
        url = self.make_url(f'/maxs/rv/alarm/alarmHandleStatusPie')
        time_range = get_time_ranges(TIME_FORMAT_1)
        start, end = time_range['最近7天']
        payload = {
            "pageIndex": 1,
            "pageSize": 10,
            "startTime": start,
            "endTime": end,
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_attack_portrait_subject(self):
        """攻击画像中间部分"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/attackPortraitSubject')
        payload = {'ip': '1.150.3.52'}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_attack_portrait_branch(self):
        """攻击画像两侧部分"""
        ip = '1.150.3.52'
        url = self.make_url(f'/maxs/rv/alarmPortrait/portraitBranch')
        payload = {'ip': ip, 'subject': 'attack'}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_attack_portrait_track(self):
        """攻击轨迹"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/pageAlarmTrack')
        ip = '1.150.3.52'
        port = '59588'
        payload = {'ip': ip, 'port': port, 'subject': 'attack', "pageIndex": 1, "pageSize": 10, }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_attack_portrait_detail(self):
        """攻击视图枝叶详情展示"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/branchDetail')
        ip = '1.150.3.52'
        victim_ip = '192.168.1.1'
        payload = {'ip': ip, 'subject': 'attack', "victimIp": victim_ip}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_victim_portrait_subject(self):
        """受害画像中间部分"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/victimPortraitSubject')
        payload = {'ip': '192.168.1.1'}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_victim_portrait_branch(self):
        """受害画像两侧部分"""
        ip = '192.168.1.1'
        url = self.make_url(f'/maxs/rv/alarmPortrait/portraitBranch')
        payload = {'ip': ip, 'subject': 'victim'}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_victim_portrait_track(self):
        """受害轨迹"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/pageAlarmTrack')
        ip = '192.168.1.1'
        port = '59588'
        payload = {'ip': ip, 'port': port, 'subject': 'victim', "pageIndex": 1, "pageSize": 10, }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def test_victim_portrait_detail(self):
        """受害视图枝叶详情展示"""
        url = self.make_url(f'/maxs/rv/alarmPortrait/branchDetail')
        ip = '192.168.1.1'
        attack_ip = '1.150.3.52'
        payload = {'ip': ip, 'subject': 'victim', "attackIp": attack_ip}
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True
