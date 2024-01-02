from .base import ClusterBaseHandler
from ..base import get_time_ranges


class ClusterStatistics(ClusterBaseHandler):
    """
    集群管理
    """

    def statistic_list(self):
        """总体信息"""
        url = self.make_url(f'/clusterOps/overview/list')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def statistic_ior(self):
        """集群IO趋势图"""
        url = self.make_url(f'/clusterOps/overview/ioReadTrend')
        times = get_time_ranges()['当天']
        data = {'startTime': times[0], 'endTime': times[1]}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def statistic_iow(self):
        """集群IO趋势图"""
        url = self.make_url(f'/clusterOps/overview/ioWriteTrend')
        times = get_time_ranges()['当天']
        data = {'startTime': times[0], 'endTime': times[1]}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def statistic_cpu(self):
        """集群CPU趋势图"""
        url = self.make_url(f'/clusterOps/overview/cpuTrend')
        times = get_time_ranges()['当天']
        data = {'startTime': times[0], 'endTime': times[1]}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def statistic_netu(self):
        """集群网络流量趋势图"""
        url = self.make_url(f'/clusterOps/overview/netTrendUp')
        times = get_time_ranges()['当天']
        data = {'startTime': times[0], 'endTime': times[1]}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def statistic_netd(self):
        """集群网络流量趋势图"""
        url = self.make_url(f'/clusterOps/overview/netTrendDown')
        times = get_time_ranges()['当天']
        data = {'startTime': times[0], 'endTime': times[1]}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True