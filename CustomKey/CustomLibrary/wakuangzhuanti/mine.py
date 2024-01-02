from itertools import product

from ..MysqlKEY import MysqlFunction
from ..base import get_time_ranges, TIME_FORMAT_1
from ..baseclass import BaseAlarmHandler


class MineHandler(BaseAlarmHandler):
    """
    挖矿
    """
    log_file = '挖矿tda.log'
    # 时间范围
    time_dict = get_time_ranges('%Y-%m-%d %H:%M')
    time_range = time_dict.values()
    # 处置状态
    handle_state = ["1", "-1", ""]

    def prepare_data(self):
        # 新增内网配置
        self.make_internal_ip()
        self.make_warns()

    def get_warns(self, page=1, page_size=10, query: dict = None) -> dict:
        """获取告警列表"""
        url = self.make_url('/maxs/rv/alarm/pageAlarm')
        time_range = get_time_ranges(TIME_FORMAT_1)
        start, end = time_range['当天']
        payload = {
            "pageIndex": page,
            "pageSize": page_size,
            "startTime": start,
            "endTime": end,
            'alarmType': ['挖矿程序']
        }
        query = query or {}
        payload.update(query)
        res = self.session.post(url=url, json=payload)
        j_res = res.json()
        return j_res

    def make_internal_ip(self):
        url = self.make_url('/maxs/acm/modelInst/save')
        data = {
            "modelId": "1381511619526828034",
            "properties": {
                "IP": "10.242.2.54-10.242.2.55",
                "AREA_ID": "3262",
                "COUNTRY": "中国",
                "PROVINCE": "新疆维吾尔自治区",
                "CITY": "克孜勒苏柯尔克孜自治州",
                "LNG": "76.172825",
                "LAT": "39.713431"
            }
        }
        res = self.session.post(url, json=data).json()
        if '范围重叠' in res['message']:
            pass
        elif res['code'] == 200:
            pass
        else:
            raise Exception(f'创建内网配置失败.url:{url}.data:{data}.res:{res}')

        conn_info = {"user": "root", "password": "maxs.PDG~2022", "host": self.master, "port": "3306",
                     "database": "SSA"}
        sql = "SELECT INNER_IP_RANGE FROM UPMS_ORGANIZATION WHERE NAME=\"默认租户总部\";"
        ip_range = MysqlFunction().get_data_in_mysql(conn_info, sql, "INNER_IP_RANGE")
        ip_range = ip_range.split(',10.242.2.54,10.242.2.55')[0]
        new_range = ip_range + ',10.242.2.54,10.242.2.55'
        sql = f"UPDATE UPMS_ORGANIZATION SET INNER_IP_RANGE=\"{new_range}\" WHERE NAME=\"默认租户总部\";"
        MysqlFunction().exec_sql_in_mysql(conn_info, sql)

        url = self.make_url('/maxs/acm/modelInst/save')
        user = self.get_user_ids()[0]
        data = {
            "modelId": "1379267039385284610",
            "properties": {
                "CHARGER_ID": "",
                "ORG_ID": "1",
                "STATUS": 1,
                "IS_KEY": 0,
                "IS_AV_INSTALL": 0,
                "IS_EXPOSED": 0,
                "IP_DETAILS": [
                    {
                        "IP": "10.242.2.54",
                        "IP_NAME": "internal1"
                    }
                ],
                "PORT_DETAILS": [],
                "CONNECTOIN_DETAILS": [],
                "DOMAIN_ID": "",
                "DEVICE_TYPE_ID": "",
                "SECURITY_DEPARTMENT_ID": "",
                "SECURITY_ADMIN": None,
                "MAINTENANCE_DEPARTMENT_ID": "",
                "MAINTENANCE_ADMIN": None,
                "DEVICE_NAME": "测试服务器1",
                "OWNER_ID": user
            }
        }

        res = self.session.post(url, json=data).json()
        if res['code'] == 200:
            pass
        elif '已存在' in res['message']:
            pass
        else:
            raise Exception(f'创建资产失败.data:{data}.res:{res}')

        data = {
            "modelId": "1379267039385284610",
            "properties": {
                "CHARGER_ID": "",
                "ORG_ID": "1",
                "STATUS": 1,
                "IS_KEY": 0,
                "IS_AV_INSTALL": 0,
                "IS_EXPOSED": 0,
                "IP_DETAILS": [
                    {
                        "IP": "10.242.2.55",
                        "IP_NAME": "internal2"
                    }
                ],
                "PORT_DETAILS": [],
                "CONNECTOIN_DETAILS": [],
                "DOMAIN_ID": "",
                "DEVICE_TYPE_ID": "",
                "SECURITY_DEPARTMENT_ID": "",
                "SECURITY_ADMIN": None,
                "MAINTENANCE_DEPARTMENT_ID": "",
                "MAINTENANCE_ADMIN": None,
                "DEVICE_NAME": "测试服务器1",
                "OWNER_ID": user
            }
        }

        res = self.session.post(url, json=data).json()
        if res['code'] == 200:
            pass
        elif '已存在' in res['message']:
            pass
        else:
            raise Exception(f'创建资产失败.data:{data}')

    def clean_data(self):
        # 还原组织内网ip
        conn_info = {"user": "root", "password": "maxs.PDG~2022", "host": self.master, "port": "3306",
                     "database": "SSA"}
        sql = "SELECT INNER_IP_RANGE FROM UPMS_ORGANIZATION WHERE NAME=\"默认租户总部\";"
        ip_range = MysqlFunction().get_data_in_mysql(conn_info, sql, "INNER_IP_RANGE")
        new_range = ip_range.split(',10.242.2.54,10.242.2.55')[0]
        sql = f"UPDATE UPMS_ORGANIZATION SET INNER_IP_RANGE=\"{new_range}\" WHERE NAME=\"默认租户总部\";"
        MysqlFunction().exec_sql_in_mysql(conn_info, sql)

        url = self.make_url('/maxs/acm/modelInst/queryPage')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "modelId": "1381511619526828034",
            "queryString": None,
            "filterGroup": {
                "condition": "AND",
                "rules": [
                    {
                        "operator": "equals",
                        "value": "10.242.2.54-10.242.2.55",
                        "key": "IP"
                    }
                ]
            }
        }
        res = self.session.post(url, json=data).json()
        if res['data']['rowData']:
            mid = res['data']['rowData'][0]['_modelId']
            id_ = res['data']['rowData'][0]['__id']

            url = self.make_url('/maxs/acm/modelInst/newDeleteByIds')
            data = {
                "modelInsts": [
                    {
                        "modelInstId": id_,
                        "modelId": mid,
                        "tenantId": ""
                    }
                ]
            }
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def overview_affected_assets(self):
        """受害资产总览"""
        url = self.make_url(f'/maxs/rv/miningView/overviewPie')
        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def mine_state(self):
        """挖矿阶段图"""
        url = self.make_url(f'/maxs/rv/miningView/stage')

        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def affected_top_five(self):
        """受害资产被攻击天数TOP5"""
        url = self.make_url(f'/maxs/rv/miningView/persistentAttackTop')

        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def mine_trend(self):
        """挖矿告警趋势"""
        url = self.make_url(f'/maxs/rv/miningView/alarmTrend')

        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def alarm_source(self):
        """告警来源"""
        url = self.make_url(f'/maxs/rv/miningView/alarmSourceBar')
        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    # @pass_unittest()
    def coins_type(self):
        """挖矿币图"""
        url = self.make_url(f'/maxs/rv/miningView/coinsTypePie')
        for tm, state in product(self.time_range, self.handle_state):
            data = {'startTime': tm[0], 'endTime': tm[1], 'alarmScope': state}
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def list_victim_assets(self):
        """挖矿受害资产列表"""
        url = self.make_url(f'/maxs/rv/miningView/pageVictimAssets')
        for tm, state in product(self.time_range, self.handle_state):
            data = {
                "startTime": tm[0],
                "endTime": tm[1],
                "alarmScope": state,
                "victimInfoIp": "",
                "assetType": "",
                "miningStage": "",
                "miningPoolIps": [],
                "miningPoolDomains": [],
                "orderAsc": False,
                "orderField": ""
            }

            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def fill_victim_assets(self):
        """查询挖矿受害资产的详细信息"""
        url = self.make_url(f'/maxs/rv/miningView/pageVictimAssets')
        s, e = self.time_dict['最近7天']
        data = {
            "startTime": s,
            "endTime": e,
            "alarmScope": "",
            "victimInfoIp": "",
            "assetType": "",
            "miningStage": "",
            "miningPoolIps": [],
            "miningPoolDomains": [],
            "orderAsc": False,
            "orderField": ""
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        ips = [i['victimIp'] for i in res['data']]
        ips = ips or ['192.168.1.1']

        url = self.make_url(f'/maxs/rv/miningView/fillVictimAssets')
        data = {
            "ips": ips,
            "startTime": s,
            "endTime": e,
            "alarmScope": "",
            "miningStage": "",
            "miningPoolIps": [],
            "miningPoolDomains": [],
            "assetType": "",
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def mining_alarms(self):
        """查询挖矿受害资产的具体告警"""
        url = self.make_url(f'/maxs/rv/miningView/pageVictimAssets')
        s, e = self.time_dict['最近7天']
        data = {
            "startTime": s,
            "endTime": e,
            "alarmScope": "",
            "victimInfoIp": "",
            "assetType": "",
            "miningStage": "",
            "miningPoolIps": [],
            "miningPoolDomains": [],
            "orderAsc": False,
            "orderField": ""
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        ips = [i['victimIp'] for i in res['data']]

        url = self.make_url(f'/maxs/rv/miningView/pageMiningAlarms')
        data = {
            "ips": ips,
            "startTime": s,
            "endTime": e,
            "alarmScope": "",
            "miningStage": "",
            "miningPoolIps": [],
            "miningPoolDomains": [],
            "assetType": "",
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def get_all_mining_domains(self):
        """查询所有矿池域名"""
        url = self.make_url(f'/maxs/rv/miningView/getAllMiningDomains')
        for tm, state in product(self.time_range, self.handle_state):
            data = {
                "startTime": tm[0],
                "endTime": tm[1],
                "alarmScope": state,
            }
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def get_all_mining_pools(self):
        """查询所有矿池地址"""
        url = self.make_url(f'/maxs/rv/miningView/getAllMiningPoolIps')
        for tm, state in product(self.time_range, self.handle_state):
            data = {
                "startTime": tm[0],
                "endTime": tm[1],
                "alarmScope": state,
            }
            res = self.session.get(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def export_mining_assets(self):
        """挖矿受害资产导出"""
        url = self.make_url(f'/maxs/rv/miningView/exportMiningAssets')
        tm = self.time_dict['最近90天']
        data = {
            "startTime": tm[0],
            "endTime": tm[1],
            "alarmScope": "",
            "victimInfoIp": "",
            "assetType": "",
            "miningPoolIps": [],
            "miningPoolDomains": []
        }
        res = self.session.post(url, json=data)
        assert res.status_code == 200, f'接口出错，url：{url}'

        return True

    def export_some_mining_assets(self):
        """挖矿受害资产指定导出"""
        url = self.make_url(f'/maxs/rv/miningView/exportPartialMiningAssets')
        tm = self.time_dict['最近90天']

        data = {
            "ips": [],
            "startTime": tm[0],
            "endTime": tm[1],
            "alarmScope": "",
        }
        res = self.session.post(url, json=data)
        assert res.status_code == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def save_column(self):
        """保存配置表格字段"""
        url = self.make_url(f'/maxs/rv/alarm/saveCustomTableColumn')

        data = {
            "tableId": "miningAssetsInfo",
            "columnsInside": "[\"ALERT_NAME\",\"RISK_LEVEL\",\"COUNT\",\"MINING_STAGE\",\"MINING_POOL\",\"ATTACKER_IP\",\"UPDATE_TIME\",\"HANDLE_RESULT\"]",
            "columnsMajor": "[\"victimIp\",\"assetName\",\"assetType\",\"assetAdministrator\",\"alarmNum\",\"lastActiveTime\",\"underAttackedDays\",\"miningPoolDomains\",\"miningPoolIps\",\"miningCurrencies\"]"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def get_column(self):
        """查询配置表格字段"""
        url = self.make_url(f'/maxs/rv/alarm/getCustomTableColumn')
        data = {"tableId": "miningAssetsInfo"}
        res = self.session.post(url, data=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        keys = list(res['data'].keys())
        keys.sort()
        f_data = {
            "pageSize": None,
            "pageIndex": None,
            "sort": None,
            "sort_key": None,
            "startLimit": None,
            "platformMg": None,
            "orgIds": None,
            "permissionId": None,
            "id": None,
            "tableId": None,
            "columnsMajor": "[\"victimIp\",\"assetName\",\"assetType\",\"assetAdministrator\",\"alarmNum\",\"lastActiveTime\",\"underAttackedDays\",\"miningPoolDomains\",\"miningPoolIps\",\"miningCurrencies\"]",
            "columnsInside": "[\"ALERT_NAME\",\"RISK_LEVEL\",\"COUNT\",\"MINING_STAGE\",\"MINING_POOL\",\"ATTACKER_IP\",\"UPDATE_TIME\",\"HANDLE_RESULT\"]",
            "columnsThird": None,
            "columnsMajorTotal": "{\"victimIp\":\"受害资产IP\",\"assetName\":\"受害资产名称\",\"assetType\":\"受害资产类型\",\"assetAdministrator\":\"资产责任人\",\"alarmNum\":\"告警数\",\"lastActiveTime\":\"最后活跃时间\",\"underAttackedDays\":\"被攻击天数\",\"miningPoolDomains\":\"矿池域名\",\"miningPoolIps\":\"矿池地址\",\"miningCurrencies\":\"挖矿币\"}",
            "columnsInsideTotal": "{\"ALERT_NAME\":\"告警名称\",\"RISK_LEVEL\":\"威胁等级\",\"COUNT\":\"攻击次数\",\"MINING_STAGE\":\"挖矿阶段\",\"MINING_POOL\":\"矿池域名\",\"ATTACKER_IP\":\"矿池地址\",\"UPDATE_TIME\":\"最后活跃时间\",\"HANDLE_RESULT\":\"处置状态\"}",
            "columnsThirdTotal": None,
            "type": None,
            "remark": None,
            "createTime": None,
            "userId": None
        }
        f_keys = list(f_data.keys())
        f_keys.sort()
        assert keys == f_keys, f'接口出错，url：{url}, res: {res}'
        return True
