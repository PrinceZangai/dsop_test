import time

from ..base import retry
from .base import ClusterBaseHandler


class ServiceManage(ClusterBaseHandler):
    """
    服务管理
    """

    def service_list(self):
        """服务列表"""
        url = self.make_url(f'/clusterOps/serviceManager/list')
        data = {
            'pageSize': 10,
            'pageIndex': 1,
            'name': '',
            'status': '',
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    @retry(3, 3)
    def service_start(self):
        """集群服务启动接口"""
        self.wait_for_service()
        id_ = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/start/{id_}')
        r = self.session.get(url)
        res = r.json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def get_service_id(self):
        return 101
        # url = self.make_url(f'/clusterOps/serviceManager/list')
        # data = {
        #     'pageSize': 10,
        #     'pageIndex': 1,
        #     'name': '',
        #     'status': '',
        # }
        # res = self.session.post(url, json=data).json()
        # res_data: list = res['data']['dataList']
        # # service = random.choice(res_data)
        # service = res_data[0]
        # service_id = service['id']
        # return service_id

    def service_stop(self):
        """集群服务停止接口"""
        self.wait_for_service()
        id_ = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/stop/{id_}')
        r = self.session.get(url)
        res = r.json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    @retry(5, 5)
    def service_restart(self):
        """集群服务重启接口"""
        self.wait_for_service()
        id_ = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/restart/{id_}')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_del(self):
        """集群服务删除接口"""
        id_ = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/del')
        data = {'id': id_}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_node_operation(self):
        """集群扩缩容接口"""
        service_id = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/nodeOperation')
        data = {
            "serviceId": service_id,
            "nodeTypeDtoList": []
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_all_list(self):
        """所有服务列表详情"""
        url = self.make_url(f'/clusterOps/serviceManager/allServiceList?taskId=')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def get_service_id_list(self):
        url = self.make_url(f'/clusterOps/serviceManager/allServiceList?taskId=')
        res = self.session.get(url).json()
        ids = [row['id'] for row in res['data']['dataList']]
        return ids

    def get_task_id(self):
        url = self.make_url(f'/clusterOps/serviceManager/allServiceList?taskId=')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return res.get('data', {}).get('taskId', '')

    def service_add(self):
        """任务添加服务接口"""
        # id_list = self.get_service_id_list()
        id_list = self.get_service_id()
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/addService')
        data = {
            'idList': id_list,
            'taskId': task_id,
        }
        res = self.session.get(url, params=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_query_property_by_ids(self):
        """获取服务属性列表接口"""
        # id_list = self.get_service_id_list()
        id_list = self.get_service_id()
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/queryPropertyByIds')
        data = {
            'idList': id_list,
            'taskId': task_id,
        }
        res = self.session.get(url, params=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_add_property(self):
        """任务添加服务属性接口"""
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/addServiceProperty')
        data = {
            "taskId": task_id,
            "propertyList": [
                {
                    "serviceId": "101",
                    "dataList": [
                        {
                            "code": "tmpdir",
                            "curValue": "/data/comm/mariadb-10.5.17-linux-x86_64/tmp",
                            "id": "1"
                        },
                        {
                            "code": "binlog_do_db",
                            "curValue": "SSA,SATP",
                            "id": "2"
                        },
                        {
                            "code": "replicate_do_db",
                            "curValue": "SSA,SATP",
                            "id": "3"
                        }
                    ]
                }
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def get_node_ids(self):
        id_list = self.get_service_id_list()
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/queryNodeListByService')
        data = {
            'idList': id_list,
            'taskId': task_id,
        }
        res = self.session.get(url, params=data).json()
        ids = [row['id'] for row in res['data']['nodeVos']]
        return ids

    def service_query_node_list_by_service(self):
        """集群服务列表接口"""
        id_list = self.get_service_id()
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/queryNodeListByService')
        data = {
            'idList': id_list,
            'taskId': task_id,
        }
        res = self.session.get(url, params=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_add_node(self):
        """任务添加服务节点接口"""
        task_id = self.get_task_id()
        node_ids = self.get_node_ids()
        url = self.make_url(f'/clusterOps/serviceManager/addServiceNode')
        data = {
            "taskId": task_id,
            "serviceNodeList": [
                {
                    "serviceId": "101",
                    "dataList": [
                        {
                            "type": "master",
                            "nodeId": node_ids[0]
                        },
                        {
                            "type": "master2",
                            "nodeId": node_ids[1]
                        },
                        {
                            "type": "slave",
                            "nodeId": node_ids[2]
                        }
                    ]
                }
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_pre_ov(self):
        """任务预览接口"""
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/preOverview')
        data = {
            "taskId": task_id,
        }
        res = self.session.get(url, params=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_task_cmt(self):
        """任务安装接口"""
        task_id = self.get_task_id()
        url = self.make_url(f'/clusterOps/serviceManager/taskCommit/{task_id}')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def wait_for_service(self):
        url = self.make_url(f'/clusterOps/serviceManager/list')
        data = {
            'pageSize': 10,
            'pageIndex': 1,
            'name': '',
            'status': '',
        }
        for _ in range(20):
            res = self.session.post(url, json=data).json()
            res_data: list = res['data']['dataList']
            if len(res_data):
                break

            time.sleep(5)
        else:
            raise Exception('创建服务安装失败')

    def service_query_task_process(self):
        """安装进度查询接口"""
        url = self.make_url(f'/clusterOps/serviceManager/queryTaskProcess')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_service_retry(self):
        """任务组件重试接口"""
        url = self.make_url(f'/clusterOps/serviceManager/queryTaskProcess')
        res = self.session.get(url).json()
        task_id = res['data']['dataList'][0]['taskId']
        service_id = res['data']['dataList'][0]['serviceId']
        url = self.make_url(f'/clusterOps/serviceManager/serviceRetry')
        data = {
            'taskId': task_id,
            'serviceId': service_id
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_download_install_log(self):
        """安装日志下载接口"""
        url = self.make_url(f'/clusterOps/serviceManager/downloadInstallLog')
        res = self.session.get(url)
        assert res.ok, f'接口出错，url：{url}, res: {res}'
        return True

    def service_update_service_property(self):
        """服务属性更新接口"""
        node_id = self.get_node_ids()[0]
        # node_id = 83
        service_id = self.get_service_id()
        url = self.make_url(f'/clusterOps/serviceManager/updateServiceProperty')
        data = {
            "nodeId": node_id,
            "propertyList": [
                {
                    "serviceId": service_id,
                    "dataList": [
                        {
                            "code": "appendfsync",
                            "curValue": "everysec",
                            "id": "4"
                        },
                        {
                            "code": "auto_aof_rewrite_percentage",
                            "curValue": "101",
                            "id": "5"
                        },
                        {
                            "code": "auto_aof_rewrite_min_size",
                            "curValue": "64mb",
                            "id": "6"
                        },
                        {
                            "code": "slowlog_log_slower_than",
                            "curValue": "10000",
                            "id": "7"
                        },
                        {
                            "code": "aof_rewrite_incremental_fsync",
                            "curValue": "yes",
                            "id": "8"
                        }
                    ]
                }
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def service_query_expand_progress(self):
        """扩容进度查询"""
        url = self.make_url(f'/clusterOps/serviceManager/queryScaleProcess')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True
