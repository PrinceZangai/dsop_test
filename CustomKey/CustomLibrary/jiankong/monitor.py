from ..baseclass import BaseHandler


class MoniHandler(BaseHandler):
    """
    采集监控
    预处理监控
    """

    def get_flume_state(self):
        """获取flume状态"""
        url = self.make_url(f'/data-access/flume/monitor/listFlumesByPage')
        data = {'name': '', 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def get_flume_name_search(self, name):
        """名称搜索flume状态"""
        url = self.make_url(f'/data-access/flume/monitor/listFlumesByPage')
        data = {'name': name, 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        assert res['total'] == 1, f'flume状态搜索失败，未出现预期数据，url：{url}, res: {res}'
        assert res['states'][0]['NAME'] == name, f'flume状态搜索失败，未出现预期数据，url：{url}, res: {res}'
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        data = {'name': name, 'state': 'EXCEPTIONAL', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def delete_flume_state(self):
        """删除flume状态"""
        url = self.make_url(f'/data-access/flume/monitor/listFlumesByPage')
        data = {'name': '', 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        states = res['states']
        if len(states) == 0:
            return True

        name = states[0]['NAME']

        url = self.make_url(f'/data-access/flume/monitor/deleteFlumeState')
        data = {'name': name}
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def get_dp_state(self):
        """获取数据处理状态"""
        url = self.make_url(f'/data-access/dataprocess/monitor/listDataprocessByPage')
        data = {'name': '', 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def get_dp_name_search(self):
        """名称搜索dp状态"""
        url = self.make_url(f'/data-access/dataprocess/monitor/listDataprocessByPage')
        data = {'name': '', 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        if res['total'] == 0:
            return True

        name = res['states'][0]['NAME']
        data = {'name': name, 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        assert res['states'][0]['NAME']==name, f'flume状态搜索失败，未出现预期数据，url：{url}, res: {res}'
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'
        assert res['total'] == 1, f'接口出错，url：{url}, res: {res}'

        return True

    def delete_dp_state(self):
        """删除数据处理状态"""
        url = self.make_url(f'/data-access/dataprocess/monitor/listDataprocessByPage')
        data = {'name': '', 'state': '', 'startPage': 1, 'pageSize': 6}
        res = self.session.post(url, data=data).json()
        states = res['states']
        if len(states) == 0:
            return True

        name = states[0]['NAME']

        url = self.make_url(f'/data-access/dataprocess/monitor/deleteDataprocessState')
        data = {'name': name}
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True
