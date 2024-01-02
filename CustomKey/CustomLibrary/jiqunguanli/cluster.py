from .base import ClusterBaseHandler
from .login import ClusterLogin
from .node import NodeManage
from .service import ServiceManage
from .statistics import ClusterStatistics
from ..base import generate_random_word


class ClusterManage(ClusterBaseHandler):
    """
    集群管理
    """

    def test_create_update(self):
        """集群创建修改接口"""
        url = self.make_url(f'/clusterOps/clusterManager/createOrUpdate')
        name = generate_random_word(8)
        data = {'name': name}
        res = self.session.post(url, data=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True


class Cluster(ClusterLogin,
              ClusterManage,
              NodeManage,
              ServiceManage,
              ClusterStatistics):
    """
    集群相关测试
    """

    def clear_all(self, v1, v2, v3):
        self.service_del()
        self.delete_nodes_if_exist()
        self.vip_delete(v1, v2, v3)
        return True
