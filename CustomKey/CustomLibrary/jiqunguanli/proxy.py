from .cluster import Cluster
from ..baseclass import BaseProxy


class ClusterProxy(BaseProxy):

    def get_clu_handler(self, *args, **kwargs):
        return self.get_handler(Cluster, *args, **kwargs)
