import json
import os

from ..base import get_ctime_str
from ..baseclass import BaseHandler


class OrderManage(BaseHandler):
    """
    工单管理
    """

    def om_flow_create(self):
        """创建流程"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000001"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        return True

    def om_flow_list(self):
        """分页展现流程"""
        url = self.make_url(f'/maxs/soar/playbook2/pagePlaybook.do')
        data = {
            "nameLike": "",
            "type": "2",
            "state": "",
            "orderBy": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_delete(self):
        """删除流程"""
        url = self.make_url(f'/maxs/soar/playbook2/pagePlaybook.do')
        data = {
            "nameLike": "",
            "type": "2",
            "state": "",
            "orderBy": "",
            "pageIndex": 1,
            "pageSize": 100
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        for row in res['data']['rowData']:
            if row['isSys'] == 0:
                continue

            rid = row['id']
            url = self.make_url(f'/maxs/soar/playbook2/deletePlaybook.do')
            data = {
                "id": rid,
            }
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_get_json(self):
        """工单详情---获取工单流程流程图"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000001"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        url = self.make_url(f'/maxs/soar/playbook2/getFlowJson.do')
        data = {
            "pbId": rid
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_save_node(self):
        """流程节点保存"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000004"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        nodes = switch_res1['data']['nodes']
        edges = switch_res1['data']['edges']

        # 结束组件id
        end_widget_id = list(filter(lambda x: x['name'] == '结束', nodes))[0]['id']
        # 结束组件的前一个节点的id
        end_widget_pre_id = list(filter(lambda x: x['id'].endswith(end_widget_id), edges))[0]['id'].split('-')[0]
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        # 挪动结束组件
        now = get_ctime_str()
        url = self.make_url(f'/maxs/soar/workflow/metadata/updateNode')
        data = {
            "name": "已结束",
            "notice": [
                "-1"
            ],
            "id": end_widget_id,
            "tenantId": -1,
            "createAcc": None,
            "createTime": None,
            "updateAcc": "me robot",
            "updateTime": now,
            "sid": None,
            "version": 1,
            "state": 1,
            "isCur": 1,
            "pbId": rid,
            "nodeType": 9,
            "ser": 0,
            "exitOnErr": 1,
            "isExitOnErr": True,
            "prevId": f",{end_widget_pre_id},",
            "prevIds": None,
            "refs": None,
            "refType": None,
            "refId": None,
            "refCode": None,
            "pvId": None,
            "pvCode": None,
            "insId": None,
            "insCode": None,
            "insIdArr": [],
            "refsArr": [],
            "conditions": None,
            "wayIn": 1,
            "isWayIn": False,
            "condRepeat": 0,
            "isRepeat": False,
            "condwait": 1,
            "condTimeType": "MIN",
            "wayOut": 1,
            "condition": [],
            "inputParam": "[]",
            "outputParam": "[]",
            "in": [],
            "out": [],
            "enable": 0,
            "valid": 1,
            "expireSLA": None,
            "owner": None,
            "manualIn": {
                "id": None,
                "tenantId": None,
                "incId": None,
                "incName": None,
                "pbId": None,
                "pbName": None,
                "nodeId": None,
                "nodeName": None,
                "nodeExeId": None,
                "inputType": None,
                "inputDesc": None,
                "input": None,
                "updateAcc": None,
                "updateTime": None,
                "expireTime": None,
                "ifExpire": 0,
                "owner": None,
                "state": None,
                "deadline": None,
                "confirmTimeout": None,
                "confirmTimeoutUnit": "hour",
                "confirmTimeoutOrigin": 1,
                "bizCode": "manual_input"
            },
            "checkMsg": None,
            "prevNodes": None,
            "nextNodes": None,
            "forValueType": "-1",
            "forSource": None,
            "nodeJson": json.dumps(nodes),
            "edgeJson": json.dumps(edges),
            "groupJson": None,
            "extendJson": "{\"notifyWay\":[\"-1\"]}",
            "extendConfig": {
                "loopCond": None,
                "loopCondStr": [],
                "loopType": 0,
                "loopAsync": False,
                "loopTimeout": 0,
                "loopTimeoutUnit": "",
                "loopTimeoutOrigin": 0,
                "async": False,
                "asyncTimeout": 0,
                "asyncTimeoutUnit": "",
                "asyncTimeoutOrigin": 0,
                "retry": False,
                "retryTimes": 0,
                "retryInterval": 0,
                "retryIntervalUnit": "",
                "retryIntervalOrigin": 0
            },
            "extendConfig2": {
                "notifyWay": [
                    "-1"
                ]
            },
            "desc": "已结束的描述",
            "srCycleParam": {
                "cycleCond": None,
                "quitCond": None,
                "overTime": None
            },
            "title": None,
            "wayInCount": 0,
            "pairId": None
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url('/maxs/soar/playbook2/standardSaveAndConcatNode.do')
        data = {
            "nodes": [],
            "edges": [],
            "uNodes": [
                {
                    "name": "已结束",
                    "label": "已结束",
                    "id": end_widget_id,
                    "pbId": rid,
                    "data": {
                        "key": "",
                        "type": "",
                        "nodeType": 9
                    },
                    "shape": "flow-start",
                    "nodeType": 9,
                    "position": {
                        "x": -100,
                        "y": 504
                    },
                    "valid": 1,
                    "refType": None,
                    "desc": "aaa"
                }
            ],
            "rEdges": []
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_pub(self):
        """发布流程"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000004"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        url = self.make_url('/maxs/soar/workflow/metadata/publish.do')
        data = {'id': rid}

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_pub_edit(self):
        """编辑已发布流程"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000004"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        url = self.make_url('/maxs/soar/workflow/metadata/publish.do')
        data = {'id': rid}

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        url = self.make_url('/maxs/soar/playbook2/getEditPubPlaybook.do')
        data = {'sid': rid}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_pub_check(self):
        """工单流程校验"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000004"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        url = self.make_url('/maxs/soar/workflow/metadata/publish.do')
        data = {
            "id": rid,
            "type": "205"
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_copy(self):
        """工单流程复制"""
        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "type": "2",
        }
        save_res1 = self.session.post(url, json=data).json()
        assert save_res1['code'] == 200, f'接口出错，url：{url}, res: {save_res1}'
        rid = save_res1['data']['id']
        url = self.make_url(f'/maxs/soar/workflow/metadata/switch.do')
        data = {
            "id": rid,
            "switchSid": "1000000000000000004"
        }
        switch_res1 = self.session.post(url, json=data).json()
        assert switch_res1['code'] == 200, f'接口出错，url：{url}, res: {switch_res1}'

        url = self.make_url(f'/maxs/soar/workflow/metadata/save.do')
        data = {
            "name": self.random_uname,
            "type": "205",
            "desc": "This is a meaningless text, just function as placeholder. --Chen Ziang.",
            "id": rid,
            "sid": rid
        }
        save_res2 = self.session.post(url, json=data).json()
        assert save_res2['code'] == 200, f'接口出错，url：{url}, res: {save_res2}'

        url = self.make_url('/maxs/soar/workflow/metadata/copy')
        data = {
            "id": rid,
        }

        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_create(self):
        """创建工单"""
        url = self.make_url('/maxs/soar/workflow/saveWorkflow.do')
        users = self.get_users(query={'name': 'test', 'pageSize': 100})
        data = {
            "woType": "1",
            "woName": self.random_uname,
            "bizType": "201",
            "woFlowId": "1000000000000000005",
            "woFlowName": "1000000000000000005",
            "woPriority": "1",
            "woDesc": "11",
            "fileList": [],
            "woFrom": 0,
            "exeType": "1",
            "srWorkflowCustomInfo": {
                "acceptor": users,
                "endTimeCount": "1",
                "endTimeUnit": "hour",
                "endTimeSecond": 3600,
                "approveFlag": "false",
                "informType": "-1"
            }
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_list(self):
        """分页查询工单列表"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        for tp in ['1', '2', '3']:
            data = {
                "pageIndex": 1,
                "pageSize": 10,
                "orderType": tp
            }
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_list_count(self):
        """查询各类型工单数量"""
        url = self.make_url('/maxs/soar/workflow/workflowCount.do')
        for tp in ['1', '2', '3']:
            data = {
                "orderType": tp
            }
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_delete(self):
        """分页查询工单列表"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '3'
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        for row in res['data']['rowData']:
            rid = row['id']
            url = self.make_url('/maxs/soar/workflow/deleteWorkflow.do')
            data = {
                "id": rid,
            }
            res = self.session.post(url, json=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_upload(self):
        """附件上传接口"""
        file = os.path.join(os.path.dirname(__file__), '工单管理.zip')
        data, headers = self.encode_file(file, field_name='fileList')
        url = self.make_url('/maxs/soar/workflow/uploadFile.do')
        res = self.session.post(url, data=data, headers=headers).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def om_download(self):
        """附件下载接口"""
        file = os.path.join(os.path.dirname(__file__), '工单管理.zip')
        data, headers = self.encode_file(file, field_name='fileList')
        url = self.make_url('/maxs/soar/workflow/uploadFile.do')
        res = self.session.post(url, data=data, headers=headers).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        old_name = res['data']['fileList'][0]['fileOldName']
        new_name = res['data']['fileList'][0]['fileNewName']

        url = self.make_url('/maxs/soar/workflow/downloadFile.do')
        params = {'fileOldName': old_name, 'fileNewName': new_name}
        res = self.session.get(url, params=params)
        assert res.ok, f'接口出错，url：{url}, res: {res}'

        return True

    def om_submit(self):
        """提交工单"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '3'
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        url = self.make_url('/maxs/soar/workflow/submitWorkflow.do')
        data = {
            "id": rid,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_retrieve(self):
        """工单详情---工单信息详情"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '3'
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        url = self.make_url('/maxs/soar/workflow/detailWorkflow.do')
        data = {
            "id": rid,
            "detailType": 0,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        url = self.make_url('/maxs/soar/workflow/detailWorkflow.do')
        data = {
            "id": rid,
            "detailType": 1,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_run(self):
        """工单流转记录"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '3'
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        url = self.make_url('/maxs/soar/workflow/workflowNodeList.do')
        data = {
            "id": rid,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_flow_chart(self):
        """获取工单流程流程图"""
        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '3'
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']
        url = self.make_url('/maxs/soar/playbook2/getFlowJson.do')
        data = {
            "pbId": rid,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def om_handle(self):
        """工单处置"""
        self.om_create()

        url = self.make_url('/maxs/soar/workflow/workflowList.do')
        data = {
            "pageIndex": 1,
            "pageSize": 10,
            "orderType": '1'
        }
        # 1收到的工单，2我发起的工单，3所有工单
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        rid = res['data']['rowData'][0]['id']

        url = self.make_url('/maxs/soar/workflow/detailWorkflow.do')
        data = {
            "id": rid,
            "detailType": 0,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        woFlowNodeId = res['data']['woFlowNodeId']
        url = self.make_url('/maxs/soar/workflow/handleWorkflow.do')
        data = {
            "handleDtolist": [
                {
                    "id": rid,
                    "woFlowNodeId": woFlowNodeId,
                    "handle": {
                        "pageIndex": None,
                        "pageSize": None,
                        "sort": None,
                        "sortKey": None,
                        "id": 1261,
                        "name": "通过",
                        "code": "pass",
                        "type": "WF-OPT",
                        "typeName": "工单操作",
                        "value": "1",
                        "description": "通过",
                        "sortIndex": None,
                        "state": 0,
                        "builtIn": 0,
                        "tenantId": -1
                    },
                    "exeMsg": "Agree.",
                    "fileList": []
                }
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True
