import os

from requests_toolbelt import MultipartEncoder

from ..base import get_time_ranges
from ..baseclass import BaseHandler


class Manage(BaseHandler):
    """
    管理
    """


class Plan(BaseHandler):
    """
    预案
    """

    def plan_add(self):
        """预案新增"""
        url = self.make_url(f'/maxs/rv/mp/warning/insertWarning')
        warning_name = "安全漏洞应对预案"
        data = {
            "warningName": warning_name,
            "warningContent": "该预案旨在应对网络安全漏洞和攻击事件，包括防火墙设置、漏洞扫描、入侵检测等措施，以及紧急响应和恢复流程。",
            "warningLevel": "2",
            "warningScope": "4"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_update(self):
        """预案修改"""
        url = self.make_url(f'/maxs/rv/mp/warning/insertWarning')
        warning_name = "灾难恢复预案"
        data = {
            "warningName": warning_name,
            "warningContent": "该预案旨在应对自然灾害、技术故障或其他紧急情况，确保组织能够快速恢复业务运作。包括备份数据、紧急联系人清单、应急资源准备等。",
            "warningLevel": "2",
            "warningScope": "4"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/mp/warning/pageWarning')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        time_range = time_dict['最近7天']
        data = {
            "pageSize": "10",
            "pageIndex": "1",
            "warningName": warning_name,
            "createUserName": "",
            "timeRange": time_range
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        w_id = res['data']['rowData'][0]['warningId']

        url = self.make_url(f'/maxs/rv/mp/warning/updateWarning')
        new_warning_name = warning_name + '_new'
        data = {
            "warningId": w_id,
            "warningName": new_warning_name,
            "warningContent": "",
            "warningLevel": "1",
            "warningScope": "3"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_list(self):
        """预案分页查询"""
        url = self.make_url(f'/maxs/rv/mp/warning/pageWarning')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        time_range = time_dict['最近7天']
        data = {
            "pageSize": "10",
            "pageIndex": "1",
            "warningName": "",
            "createUserName": "",
            "timeRange": time_range
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def plan_delete(self):
        """预案删除"""
        url = self.make_url(f'/maxs/rv/mp/warning/insertWarning')
        warning_name = "员工紧急离职预案"
        data = {
            "warningName": warning_name,
            "warningContent": "该预案旨在应对员工突然离职的情况，包括离职手续、知识转移、重新分配工作任务等，以确保组织的运营不受影响。",
            "warningLevel": "2",
            "warningScope": "4"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/mp/warning/pageWarning')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        time_range = time_dict['最近7天']
        data = {
            "pageSize": "10",
            "pageIndex": "1",
            "warningName": warning_name,
            "createUserName": "",
            "timeRange": time_range
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        w_id = res['data']['rowData'][0]['warningId']

        url = self.make_url(f'/maxs/rv/mp/warning/deleteWarning')
        data = {"warningId": w_id}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_get_tem(self):
        """预案导入模版下载"""
        url = self.make_url(f'/maxs/rv/mp/warning/downloadTemplate')
        res = self.session.get(url)
        assert res.ok, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_import(self):
        """预案文件导入"""
        url = self.make_url(f'/maxs/rv/mp/warning/import')
        file = os.path.join(os.path.dirname(__file__), '预案导入.xlsx')
        f = open(file, 'rb')
        fields = {'file': (file, f.read(), 'application/octet-stream')}
        f.close()
        multipartEncoder = MultipartEncoder(fields=fields)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': multipartEncoder.content_type
        }
        res = self.session.post(url, data=multipartEncoder, headers=headers).json()

        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_err(self):
        """错误数据下载"""
        url = self.make_url(f'/maxs/rv/mp/warning/errorData')
        res = self.session.get(url)
        assert res.ok, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_col_get(self):
        """预案自定义列查询"""
        url = self.make_url(f'/maxs/rv/alarm/getCustomTableColumn')
        res = self.session.post(url)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_col_set(self):
        """预案自定义列查询"""
        url = self.make_url(f'/maxs/rv/alarm/saveCustomTableColumn')
        data = {
            "columnsMajor": "[\"WARNING_NAME\", \"WARNING_LEVEL\", \"WARNING_SCOPE\" ,\"CREATE_USER_NAME\", \"CREATE_TIME\"]",
            "columnsInside": "{}", "tableId": "mpwarning"}
        res = self.session.post(url, json=data)
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def plan_clean(self):
        """测完清数据"""
        url = self.make_url(f'/maxs/rv/mp/warning/pageWarning')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        time_range = time_dict['最近7天']
        data = {
            "pageSize": "10",
            "pageIndex": "1",
            "warningName": "",
            "createUserName": "",
            "timeRange": time_range
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        ids = [row['warningId'] for row in res['data']['rowData']]
        for id_ in ids:
            url = self.make_url(f'/maxs/rv/mp/warning/deleteWarning')
            data = {"warningId": id_}
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True


class Workbench(BaseHandler):
    """
    工作台
    """

    def wb_alarm(self):
        """监测概况 - 安全告警"""
        url = self.make_url(f'/maxs/rv/mp/workbench/monitorOverViewAlarm')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_event(self):
        """监测概况 - 安全事件"""
        url = self.make_url(f'/maxs/rv/mp/workbench/monitorOverViewEvent')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_freq(self):
        """高频攻击者TOP5"""
        url = self.make_url(f'/maxs/rv/mp/workbench/attackTop5')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_asset(self):
        """高频受害者TOP5"""
        url = self.make_url(f'/maxs/rv/mp/workbench/victimTop5')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_ban_list(self):
        """封禁名单"""
        url = self.make_url(f'/maxs/soar/bizBlock/pageBizBlock.do')
        time_dict = get_time_ranges('%Y-%m-%d %H:%M:%S')
        t = time_dict['最近7天']
        data = {"pageIndex": 1, "pageSize": 10, "isCur": 1, "time": t}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_pre(self):
        """重保预案"""
        url = self.make_url(f'/maxs/rv/mp/workbench/pageWarning')
        data = {"pageIndex": 1, "pageSize": 10, "mpInfoId": "1223"}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_ad(self):
        """通讯录"""
        url = self.make_url(f'/maxs/rv/mp/workbench/pageAddressBook')
        data = {"pageIndex": 1, "pageSize": 10, "mpInfoId": "1223"}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_weak(self):
        """弱口令列表"""
        url = self.make_url(f'/maxs/rv/mp/workbench/listWeakPassword')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_fishing(self):
        """钓鱼邮件"""
        url = self.make_url(f'/maxs/rv/mp/workbench/listFishing')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_webshell(self):
        """Webshell"""
        url = self.make_url(f'/maxs/rv/mp/workbench/listWebShell')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        s, e = time_dict['最近7天']
        data = {"startTime": s, "endTime": e}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def wb_clean(self):
        """测完清数据"""
        url = self.make_url(f'/maxs/rv/mp/warning/pageWarning')
        time_dict = get_time_ranges("%Y-%m-%d %H:%M:%S")
        time_range = time_dict['最近7天']
        data = {
            "pageSize": "10",
            "pageIndex": "1",
            "warningName": "",
            "createUserName": "",
            "timeRange": time_range
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        ids = [row['warningId'] for row in res['data']['rowData']]
        for id_ in ids:
            url = self.make_url(f'/maxs/rv/mp/warning/deleteWarning')
            data = {"warningId": id_}
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True


class AddressBook(BaseHandler):
    """
    通讯录
    """

    # @pass_unittest()
    def ab_add(self):
        """通讯录新增"""
        url = self.make_url(f'/maxs/rv/mp/addressBook/insertAddressBook')
        username = self.random_uname
        data = {"userName": username, "belongUnit": "亚信",
                "position": "安全工程师", "telephone": "13812321341",
                "email": "10000@qq.com", "userNote": "生物自然基金获奖者", 'id': None}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def ab_update(self):
        """通讯录修改"""
        username = self.random_uname
        url = self.make_url(f'/maxs/rv/mp/addressBook/insertAddressBook')
        data = {"userName": username, "belongUnit": "亚信",
                "position": "安全工程师", "telephone": "13812321341",
                "email": "10000@qq.com", "userNote": "生物自然基金获奖者", 'id': None}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/mp/addressBook/pageAddressBook')
        data = {
            "name": username,
            "position": None,
            "belongUnit": None,
            "telephone": None,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        record_id = res['data']['rowData'][0]['id']

        new_username = self.random_uname
        url = self.make_url(f'/maxs/rv/mp/addressBook/updateAddressBook')
        data = {"id": record_id, "userName": new_username, "belongUnit": "亚信",
                "position": "安全工程师", "telephone": "13812321341",
                "email": "10000@qq.com", "userNote": "生物自然基金获奖者"}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def ab_list(self):
        """通讯录分页查询"""
        url = self.make_url(f'/maxs/rv/mp/addressBook/pageAddressBook')
        data = {
            "name": "",
            "position": None,
            "belongUnit": None,
            "telephone": None,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def ab_delete(self):
        """通讯录删除"""
        url = self.make_url(f'/maxs/rv/mp/addressBook/insertAddressBook')
        username = self.random_uname
        data = {"userName": username, "belongUnit": "亚信",
                "position": "安全工程师", "telephone": "13812321341",
                "email": "10000@qq.com", "userNote": "生物自然基金获奖者", 'id': None}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url(f'/maxs/rv/mp/addressBook/pageAddressBook')
        data = {
            "name": username,
            "position": None,
            "belongUnit": None,
            "telephone": None,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        record_id = res['data']['rowData'][0]['id']

        url = self.make_url(f'/maxs/rv/mp/addressBook/deleteAddressBook')
        data = {"id": record_id}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def ab_col_get(self):
        """自定义列查询"""
        url = self.make_url(f'/maxs/rv/alarm/getCustomTableColumn')
        data = {'tableId': 'mpaddress'}
        res = self.session.post(url, data=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def ab_col_set(self):
        """自定义列保存"""
        url = self.make_url(f'/maxs/rv/alarm/saveCustomTableColumn')
        data = {
            "columnsMajor": "[\"USER_NAME\", \"BELONG_UNIT\", \"POSITION\" ,\"TELEPHONE\", \"EMAIL\", \"USER_NOTE\"]",
            "columnsInside": "{}", "tableId": "mpaddress"}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def ab_clean(self):
        """测完清数据"""
        url = self.make_url(f'/maxs/rv/mp/addressBook/pageAddressBook')
        data = {
            "name": "",
            "position": None,
            "belongUnit": None,
            "telephone": None,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        record_ids = [row['id'] for row in res['data']['rowData']]

        for record_id in record_ids:
            url = self.make_url(f'/maxs/rv/mp/addressBook/deleteAddressBook')
            data = {"id": record_id}
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True


class ProtectHandler(Manage,
                     Plan,
                     Workbench,
                     AddressBook):
    """
    重保
    """
