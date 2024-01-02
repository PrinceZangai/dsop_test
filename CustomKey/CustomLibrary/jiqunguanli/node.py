import os
import time

from ..baseclass import BaseHandler
from .base import ClusterBaseHandler


class NodeManage(ClusterBaseHandler):
    """
    节点管理
    """

    def test_list_node(self):
        """节点管理列表查询"""
        url = self.make_url(f'/clusterOps/nodeManager/list')
        data = {
            "name": "",
            "status": "",
            "sortColumn": "",
            "sortType": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def get_node_id(self):
        url = self.make_url(f'/clusterOps/nodeManager/list')
        data = {
            "name": "",
            "status": "",
            "sortColumn": "",
            "sortType": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        node_id = res['data']['dataList'][0]['id']
        return node_id

    def get_service_by_node(self):
        """节点获取服务列表查询"""
        node_id = self.get_node_id()
        url = self.make_url(f'/clusterOps/nodeManager/queryServiceByNodeId')
        data = {
            'id': node_id,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def batch_shut_down(self):
        """节点批量关机"""
        node_id = 0
        url = self.make_url(f'/clusterOps/nodeManager/batchShutdown/')
        data = [node_id]
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def delete_nodes_if_exist(self):
        url = self.make_url(f'/clusterOps/nodeManager/list')
        data = {
            "name": "",
            "status": "",
            "sortColumn": "",
            "sortType": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        for row in res['data']['dataList']:
            node_id = row['id']
            url = self.make_url(f'/clusterOps/nodeManager/delete/{node_id}')

            res = self.session.get(url).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

    def delete_node(self, node_ids):
        """节点删除"""
        try:
            self.create_by_batch_no(node_ids)
        except:
            pass

        url = self.make_url(f'/clusterOps/nodeManager/list')
        data = {
            "name": "",
            "status": "",
            "sortColumn": "",
            "sortType": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        for row in res['data']['dataList']:
            node_id = row['id']
            url = self.make_url(f'/clusterOps/nodeManager/delete/{node_id}')

            res = self.session.get(url).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def test_prefix(self):
        """节点前缀查询"""
        url = self.make_url(f'/clusterOps/nodeManager/prefix')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def get_prefix(self):
        url = self.make_url(f'/clusterOps/nodeManager/prefix')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        prefix = res['data']
        return prefix

    def test_create_node(self, node_ips):
        """新增节点"""

        url = self.make_url(f'/clusterOps/nodeManager/create')
        prefix = self.get_prefix()
        data = {
            "batchNo": "",
            "idList": [],
            "ip": node_ips,
            "passwd": "coitXNrM3UKSYpdztN84Pla6pfjFbVnV1ib+2DPbXo7uMGbs6pLheZXU5LxJusWrTiajYP5mgTqv9jCzOVqgocrs9NUg3LliSHhmW5Oh8Y9jT5sgcjiNQQKyDvejEJ4AIIW1CdAmef7BZ+aIFxIqitaAgTFM45430kauevN+lZA=",
            "port": "22",
            "prefix": prefix,
            "username": "root"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def query_by_batch_no(self, node_ips: str):
        """根据batchNo获取节点列表"""
        url = self.make_url(f'/clusterOps/nodeManager/queryByBatchNo')
        batch_no = self.get_batch_no(node_ips)
        data = {
            'batchNo': batch_no,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def get_batch(self, node_ips: str):
        url = self.make_url(f'/clusterOps/nodeManager/create')
        prefix = self.get_prefix()
        data = {
            "batchNo": "",
            "idList": [],
            "ip": node_ips,
            "passwd": "coitXNrM3UKSYpdztN84Pla6pfjFbVnV1ib+2DPbXo7uMGbs6pLheZXU5LxJusWrTiajYP5mgTqv9jCzOVqgocrs9NUg3LliSHhmW5Oh8Y9jT5sgcjiNQQKyDvejEJ4AIIW1CdAmef7BZ+aIFxIqitaAgTFM45430kauevN+lZA=",
            "port": "22",
            "prefix": prefix,
            "username": "root"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        batch = res['data']
        return batch

    def get_batch_no(self, node_ips):
        batch = self.get_batch(node_ips)
        batch_no = batch['batchNo']
        return batch_no

    def reconnect_by_id(self, node_ips):
        """重试接口"""
        batch = self.get_batch(node_ips)
        node_ids = [i['id'] for i in batch['dataList']]
        url = self.make_url(f'/clusterOps/nodeManager/reconnectById')
        data = {
            'idList': node_ids,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def remove_by_id(self, node_ips):
        """移除接口"""
        url = self.make_url(f'/clusterOps/nodeManager/removeById')

        batch = self.get_batch(node_ips)
        node_ids = [i['id'] for i in batch['dataList']]

        data = {
            'idList': node_ids[0:1],
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def add_op_machine(self):
        """新增操作机"""
        url = self.make_url(f'/clusterOps/nodeManager/list')
        data = {
            "name": "",
            "status": "",
            "sortColumn": "",
            "sortType": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res = self.session.post(url, json=data).json()
        node_id = res['data']['dataList'][0]['id']

        url = self.make_url('/clusterOps/nodeManager/addOperator')
        data = {
            'operaList': [node_id],
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def create_by_batch_no(self, node_ips):
        """新增最终提交接口"""
        batch_no = self.get_batch_no(node_ips)
        url = self.make_url(f'/clusterOps/nodeManager/queryByBatchNo')
        data = {
            'batchNo': batch_no,
        }
        for _ in range(20):
            res = self.session.post(url, json=data).json()
            rows = res['data']['dataList']
            status_list = [row['status'] for row in rows]
            if status_list.count('检测成功') == len(status_list):
                print(f'本次节点检测成功.原始响应:{res}')
                break

            print(f'本次节点检测失败，5s后重试.原始响应:{res}')
            time.sleep(5)
            continue

        url = self.make_url(f'/clusterOps/nodeManager/createByBatchNo')
        data = {
            'batchNo': batch_no,
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def download_example(self):
        """下载批量上传Excel样例接口"""
        url = self.make_url(f'/clusterOps/nodeManager/downloadExample?holeType=1')
        res = self.session.get(url)
        assert res.ok, f'接口出错，url：{url}, res: {res}'

        return True

    def node_upload(self):
        """批量上传接口"""
        url = self.make_url(f'/clusterOps/nodeManager/upload')
        excel = os.path.join(os.path.dirname(__file__), 'NodeExample.xlsx')
        encoder, headers = BaseHandler.encode_file(excel)
        res = self.session.post(url, data=encoder, headers=headers).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def stop_by_id(self):
        """停服务接口"""
        node_id = self.get_node_id()
        url = self.make_url(f'/clusterOps/nodeManager/stopById')
        data = {'id': node_id}
        res = self.session.post(url, json=data)
        assert res.ok, f'接口出错，url：{url}, res: {res}'
        return True

    def start_by_id(self):
        """启动服务接口"""
        node_id = self.get_node_id()
        url = self.make_url(f'/clusterOps/nodeManager/startById')
        data = {'id': node_id}
        res = self.session.post(url, json=data)
        assert res.ok, f'接口出错，url：{url}, res: {res}'
        return True

    def restart_by_id(self):
        """重启服务接口"""
        node_id = self.get_node_id()
        url = self.make_url(f'/clusterOps/nodeManager/restartById')
        data = {'id': node_id}
        res = self.session.post(url, json=data)
        assert res.ok, f'接口出错，url：{url}, res: {res}'
        return True

    def download_log(self):
        """下载日志服务接口"""
        url = self.make_url(f'/clusterOps/serviceManager/list')
        data = {
            'pageSize': 10,
            'pageIndex': 1,
            'name': '',
            'status': '',
        }
        res = self.session.post(url, json=data).json()

        id_ = res['data']['dataList'][0]['dataList'][0]['id']
        url = self.make_url('/clusterOps/nodeManager/downloadLog')
        data = {'id': id_}
        res = self.session.post(url, json=data)
        assert res.ok, f'接口出错，url：{url}, res: {res}'
        return True

    def passwd_verify(self):
        """删除操作的密码验证"""
        url = self.make_url('/clusterOps/nodeManager/passwdVerify')
        res = self.session.post(url, data=self.pwd).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def vip_create(self, flume_vip, inner_vip, vip):
        """vip添加"""
        url = self.make_url('/clusterOps/vip/add')
        data = {
            'vipList': [
                {
                    "ipv4": flume_vip,
                    "type": "flume_vip"
                },
                {
                    "ipv4": inner_vip,
                    "type": "inner_vip"
                },
                {
                    "ipv4": vip,
                    "type": "vip"
                }
            ]
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def vip_delete(self, flume_vip, inner_vip, vip):
        """vip删除"""
        try:
            self.vip_create(flume_vip, inner_vip, vip)
        except:
            pass

        url = self.make_url('/clusterOps/vip/list?ipv4=&type=')
        res = self.session.get(url).json()
        url = self.make_url('/clusterOps/vip/del')
        for row in res['data']:
            rid = row['id']
            data = {'ids': rid}
            res = self.session.post(url, params=data).json()
            assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def vip_update(self):
        """vip修改"""
        url = self.make_url('/clusterOps/vip/list?ipv4=&type=')
        res = self.session.get(url).json()
        record = res['data'][0]
        data = {
            "vipList": [
                {
                    "id": record['id'],
                    "ipv4": record['ipv4'],
                    "type": record['type']
                }
            ]
        }
        url = self.make_url('/clusterOps/vip/update')
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def vip_list(self):
        """vip查询"""
        url = self.make_url('/clusterOps/vip/list?ipv4=&type=')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True
