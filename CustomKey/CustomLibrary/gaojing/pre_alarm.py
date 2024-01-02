import os

from ..baseclass import BaseAlarmHandler


class PreAlarmHandler(BaseAlarmHandler):
    """
    预警管理
    """

    def pre_alarm_create(self):
        """预警新增"""
        orgs = self.get_org_tree()
        org_ids = ','.join([str(i['ID']) for i in orgs])
        url = self.make_url('/maxs/rv/pa/preAlarm/insertPredictAlarm')
        data = {
            "prealarmName": self.random_uname,
            "prealarmType": 1,
            "prealarmLevel": 1,
            "incidence": 1,
            "incidenceType": 1,
            "threatWay": 2,
            "incidenceBusi": "",
            "incidenceDomain": "",
            "incidenceOrg": "",
            "incidenceIps": "",
            "detail": "危险漏洞的预警",
            "preventionMeasure": "危险程度极高",
            "signFlag": 1,
            "publishType": "-1,0,1,2",
            "orgIds": org_ids,
            "overTime": "2023-12-31 00:00:00",
            "fileList": []
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_list(self):
        """预警下发分页查询"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmSed')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_recv_list(self):
        """预警接收分页查询"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmRec')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_recv_q(self):
        """下发预警-签收详情列表"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmSed')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        url = self.make_url('/maxs/rv/pa/preAlarm/predictAlarmRecQuery')
        data = {
            "id": rid,
            "pageSize": 10,
            "pageIndex": 1,
            "signStatus": "1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_detail(self):
        """预警详情"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmSed')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']

        url = self.make_url('/maxs/rv/pa/preAlarm/detailPredictAlarm')
        data = {
            "id": rid
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def pre_alarm_sign(self):
        """预警签收"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmRec')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        oid = res['data']['rowData'][0]['preOrgId']

        url = self.make_url('/maxs/rv/pa/preAlarm/signPredictAlarm')
        data = {
            "id": rid,
            "preOrgId": oid,
            "signComment": "-"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def pre_alarm_upload(self):
        """附件上传接口"""
        file = os.path.join(os.path.dirname(__file__), '告警预案.zip')
        data, headers = self.encode_file(file)
        url = self.make_url('/maxs/rv/pa/preAlarm/uploadFile')
        res = self.session.post(url, data=data, headers=headers).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def pre_alarm_download(self):
        """附件下载接口"""
        file = os.path.join(os.path.dirname(__file__), '告警预案.zip')
        data, headers = self.encode_file(file)
        url = self.make_url('/maxs/rv/pa/preAlarm/uploadFile')
        res = self.session.post(url, data=data, headers=headers).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        old_name = res['data']['file']['fileOldName']
        new_name = res['data']['file']['fileNewName']

        url = self.make_url('/maxs/rv/pa/preAlarm/downloadFile')
        params = {'fileOldName': old_name, 'fileNewName': new_name}
        res = self.session.get(url, params=params)
        assert res.ok, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_delete_batch(self):
        """批量删除"""
        url = self.make_url('/maxs/rv/pa/preAlarm/pagePredictAlarmRec')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderBy": "od1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        ids = [i['id'] for i in res['data']['rowData']]

        url = self.make_url('/maxs/rv/pa/preAlarm/delPredictAlarmBatch')
        data = {
            "ids": ids
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def pre_alarm_query_id(self):
        """ip查询"""

        url = self.make_url('/maxs/rv/pa/preAlarm/pageIplist')
        data = {
            "ip": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True
