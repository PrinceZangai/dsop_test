from ..MysqlKEY import MysqlFunction
from ..base import pass_unittest
from ..baseclass import BaseHandler


class NotifyRuleHandler(BaseHandler):
    """
    通知管理-规则
    """

    def nr_check_robot(self):
        """校验机器人是否可用"""
        url = self.make_url(f'/maxs/pm/messageRule/checkRobot')
        p = {'type': 'wchat'}
        res = self.session.get(url, params=p).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_create_rule(self):
        user_data = self.get_users()
        users = [{'userId': row['userId'], 'email': row['email']} for row in user_data]
        role_ids = [{'roleId': i} for i in self.get_role_ids()]
        template = self.create_nr_temp()
        data = {
            "ruleName": self.random_uname,
            "messageType": "1",
            "templateId": template,
            "ruleCondition": "{\"condition\":\"AND\",\"groups\":[{\"condition\":\"AND\",\"rules\":[{\"key\":\"TASK_NAME\",\"operator\":\"CONTAIN\",\"value\":\"a\"}]}]}",
            "channelIds": [
                -1,
                3
            ],
            "chIds": "-1,3",
            "users": users,
            "roles": role_ids,
            "dds": [],
            "emails": [],
            "wchats": [
                {
                    "channelId": 3,
                    "channelName": "微信通道",
                    "wchats": [
                        ""
                    ]
                }
            ],
            "wchatNoticeSystem": 1,
            "wchatNoticeOther": 0,
            "wchatNoticeRobot": 0
        }
        url = self.make_url('/maxs/pm/messageRule/saveOrUpdate')
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_list(self):
        """分页查询规则"""
        url = self.make_url(f'/maxs/pm/messageRule/page')
        payload = {
            "ruleName": "",
            "templateId": "",
            "channelId": "",
            "messageType": 1,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_retrieve(self):
        """查看规则详情"""
        # 列表页拿个rule id
        url = self.make_url(f'/maxs/pm/messageRule/page')
        payload = {
            "ruleName": "",
            "templateId": "",
            "channelId": "",
            "messageType": 1,
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        rule_id = res['data']['rowData'][0]['id']

        url = self.make_url(f'/maxs/pm/messageRule/getRuleDetail')
        payload = {
            "id": rule_id
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_role_user_num(self):
        """获取角色配置的用户数"""
        url = self.make_url(f'/maxs/pm/messageRule/getUserCountByRole')
        payload = {
            "roleName": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_get_temp_by_rule(self):
        """查询被规则引用的通知模板"""
        url = self.make_url(f'/maxs/pm/messageRule/getTemplateByRuleId')
        payload = {
            "type": 1,
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def create_nr_temp(self):
        """
        创建消息通知模板
        :return: 模板id
        """
        data = {
            "templateName": self.random_uname,
            "messageType": "1",
            "messageContent": "[{\"text\":\"It is a international news.\",\"type\":0},{\"text\":\" \",\"type\":0},{\"text\":\"1213\",\"type\":1},{\"text\":\" \",\"type\":0}]",
            "messageSubject": "some important topic",
            "templateType": 1
        }
        url = self.make_url('/maxs/pm/messageTemplate/saveOrUpdate')
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return res['data']

    def nr_get_dup(self):
        """获取重复设置"""
        url = self.make_url(f'/maxs/pm/messageRule/getDup')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    @pass_unittest
    def nr_update_dup(self):
        """更新重复设置"""
        url = self.make_url(f'/maxs/pm/messageRule/updateDup')
        data = {
            "code": "0",
            "dup": 0
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nr_delete(self):
        """删除规则"""
        url = self.make_url(f'/maxs/pm/messageRule/page')
        payload = {
            "ruleName": "",
            "templateId": "",
            "channelId": "",
            "messageType": 1,
            "pageIndex": 1,
            "pageSize": 100
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        rules = [{'id': i['id'], 'ruleName': i['ruleName']} for i in res['data']['rowData']]

        url = self.make_url(f'/maxs/pm/messageRule/delete')
        data = {
            "rules": rules
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True


class NotifyTunnelHandler(BaseHandler):
    """
    通知管理-通道
    """

    def nt_list(self):
        """获取全部通道（包含系统通知）"""
        url = self.make_url(f'/maxs/pm/messageChannel/getAll')
        payload = {
            "channelName": ""
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_list_open(self):
        """获取所有已启用的通道（包含系统通知）"""
        url = self.make_url(f'/maxs/pm/messageChannel/getAllChannels')
        payload = {
            "channelName": ""
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_retrieve(self):
        """查询通道信息"""
        url = self.make_url(f'/maxs/pm/messageChannel/getById')
        payload = {
            "id": 1
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_cns(self):
        """查询通知通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/list')
        payload = {
            "channelName": "",
            "status": None
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_list_page(self):
        """分页查询通知通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/page')
        payload = {
            "channelName": "",
            "status": None
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_update(self):
        """编辑通知通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/saveOrUpdate')
        payload = {
            "id": 3,
            "channelName": "微信通道",
            "channelType": 2,
            "emailSmtpAddr": None,
            "emailSmtpPort": 0,
            "emailAccount": None,
            "emailPasswd": None,
            "emailSsl": None,
            "ddAddr": None,
            "ddRobotAddr": None,
            "ddAppId": None,
            "ddAppKey": None,
            "ddAppSecret": None,
            "wchatAddr": "1",
            "wchatRobotAddr": "1",
            "wchatAppId": "1",
            "wchatCorpId": "1",
            "wchatAppSecret": "1"
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_start_stop(self):
        """启用-停用通知通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/startStop')
        payload = {
            "channels": [{
                "id": 3,
                "channelName": "微信通道",
                "channelType": 2,
                "emailSmtpAddr": None,
                "emailSmtpPort": 0,
                "emailAccount": None,
                "emailPasswd": None,
                "emailSsl": None,
                "ddAddr": None,
                "ddRobotAddr": None,
                "ddAppId": None,
                "ddAppKey": None,
                "ddAppSecret": None,
                "wchatAddr": "1",
                "wchatRobotAddr": "1",
                "wchatAppId": "1",
                "wchatCorpId": "1",
                "wchatAppSecret": "1"}]
            , "status": 1
        }
        res = self.session.post(url, json=payload).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_summary(self):
        """汇总通道数据"""
        url = self.make_url(f'/maxs/pm/messageChannel/summary')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_test_connect(self):
        """连接测试通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/testConnect')
        data = {
            "id": 3,
            "channelName": "微信通道",
            "channelType": 2,
            "emailSmtpAddr": None,
            "emailSmtpPort": 0,
            "emailAccount": None,
            "emailPasswd": None,
            "emailSsl": None,
            "ddAddr": None,
            "ddRobotAddr": None,
            "ddAppId": None,
            "ddAppKey": None,
            "ddAppSecret": None,
            "wchatAddr": "1",
            "wchatRobotAddr": "1",
            "wchatAppId": "1",
            "wchatCorpId": "1",
            "wchatAppSecret": "1"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nt_delete(self):
        """删除通知通道"""
        url = self.make_url(f'/maxs/pm/messageChannel/delete')
        data = {
            "channels": [{
                "id": 3,
                "channelName": "微信通道",
                "channelType": 2,
                "emailSmtpAddr": None,
                "emailSmtpPort": 0,
                "emailAccount": None,
                "emailPasswd": None,
                "emailSsl": None,
                "ddAddr": None,
                "ddRobotAddr": None,
                "ddAppId": None,
                "ddAppKey": None,
                "ddAppSecret": None,
                "wchatAddr": "1",
                "wchatRobotAddr": "1",
                "wchatAppId": "1",
                "wchatCorpId": "1",
                "wchatAppSecret": "1"}]
        }
        res = self.session.post(url, json=data).json()
        assert res['data']['desc'] == '删除成功！', f'接口出错，url：{url}, res: {res}'
        return True

    def nt_recovery(self):
        """数据恢复"""
        sql = """INSERT INTO `SSA`.`MESSAGE_CHANNEL`(`ID`, `CHANNEL_NAME`, `CHANNEL_TYPE`, `STATUS`, `CONNECT_STATUS`, `CONNECT_RESULT`, `CREATE_TIME`, `UPDATE_TIME`, `EMAIL_SMTP_ADDR`, `EMAIL_SMTP_PORT`, `EMAIL_ACCOUNT`, `EMAIL_PASSWD`, `EMAIL_SSL`, `DD_ADDR`, `DD_ROBOT_ADDR`, `DD_APP_KEY`, `DD_APP_ID`, `DD_APP_SECRET`, `WCHAT_ADDR`, `WCHAT_ROBOT_ADDR`, `WCHAT_APP_ID`, `WCHAT_CORP_ID`, `WCHAT_APP_SECRET`, `TENANT_ID`) VALUES (3, '微信通道', 2, 0, -1, '', '2023-08-16 09:56:50', '2023-12-07 17:24:32', NULL, '0', NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, '1', '1', '1', '1', '1', -1);"""
        conn_info = {"user": "root", "password": "maxs.PDG~2022", "host": self.master, "port": "3306",
                     "database": "SSA"}
        MysqlFunction().exec_sql_in_mysql(conn_info, sql)

        return True


class NotifyTempHandler(BaseHandler):
    """
    通知管理-模板
    """

    def nte_dict(self):
        """查询标签"""
        url = self.make_url(f'/maxs/pm/messageTemplate/dictByType')
        data = {
            "type": "MSG_PLAYBOOK"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nte_all(self):
        """查询所有模板"""
        url = self.make_url(f'/maxs/pm/messageTemplate/getAll')
        data = {
            "type": "MSG_PLAYBOOK"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nte_list(self):
        """分页查询模板"""
        url = self.make_url(f'/maxs/pm/messageTemplate/page')
        data = {
            "templateName": "",
            "messageType": "",
            "pageIndex": 1,
            "pageSize": 20
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nte_create(self):
        """新增-编辑模板"""
        data = {
            "templateName": self.random_uname,
            "messageType": "1",
            "messageContent": "[{\"text\":\"It is a international news.\",\"type\":0},{\"text\":\" \",\"type\":0},{\"text\":\"1213\",\"type\":1},{\"text\":\" \",\"type\":0}]",
            "messageSubject": "some important topic",
            "templateType": 1
        }
        url = self.make_url('/maxs/pm/messageTemplate/saveOrUpdate')
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nte_delete(self):
        """删除模板"""

        url = self.make_url(f'/maxs/pm/messageTemplate/page')
        data = {
            "templateName": "",
            "messageType": "",
            "pageIndex": 1,
            "pageSize": 100
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        templates = [{'id': i['id'], 'templateName': i['templateName']} for i in res['data']['rowData']]
        data = {
            "templates": templates
        }
        url = self.make_url('/maxs/pm/messageTemplate/delete')
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True


class NotifyRecordHandler(BaseHandler):
    def nre_top(self):
        """查询通知记录前99条"""

        url = self.make_url(f'/maxs/pm/messageRecoard/top99')
        data = {
            "messageType": "",
            "readed": 0
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nre_read(self):
        """读消息"""

        url = self.make_url(f'/maxs/pm/messageRecoard/read')
        data = {
            "ids": [
                "1732924970480552290"
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nre_count(self):
        """未读数量"""

        url = self.make_url(f'/maxs/pm/messageRecoard/getUnReadCount')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nre_enum(self):
        """获取筛选条件枚举值"""

        url = self.make_url(f'/maxs/pm/messageRecoard/getEnum')
        data = {'type': '6'}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def nre_delete(self):
        """删除消息"""

        url = self.make_url(f'/maxs/pm/messageRecoard/delete')
        data = {
            "ids": [
                "1732924970480552290"
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True


class NotifyHandler(NotifyRuleHandler,
                    NotifyTunnelHandler,
                    NotifyTempHandler,
                    NotifyRecordHandler):
    pass
