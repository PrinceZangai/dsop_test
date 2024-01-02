from ..baseclass import BaseHandler


class BiUser:
    def __init__(self):
        self.uid: str = ''
        self.org: str = '88d79672963748d98213dac5f776d5fe'


class BiBase(BaseHandler):
    def __init__(self, domain, cookies, master=None, context=None):
        super(BiBase, self).__init__(domain, cookies, master, context)
        self.bi_user = BiUser()
        # TODO:开发完删除
        self.session.headers.update({
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0NDAiLCJwYXNzd29yZCI6NDU5NzgwMzM5LCJleHAiOjE3MDI5NzQzODh9.74YO6iL8-B0HZrgb0vT5aa_91ajRK_JGxGP7EF7JD6w'})


class BiSso(BiBase):
    def sso_login(self):
        """
        单点登录接口
        {
          "avatar": null,
          "description": "MAXS_ADMIN",
          "email": "113@qq.com",
          "id": "1736677153567223809",
          "name": "test36",
          "orgOwner": false,
          "username": "test36"
        }
        """
        url = self.make_url('/maxs/bi/engine/bi-users/maxsSsoBI')
        res = self.session.post(url)
        assert res.ok, f'BI SSO登录MAXS失败.response:{res.text}'

        auth = res.headers['Authorization']
        self.session.headers.update({'Authorization': auth})

        jres = res.json()['data']
        self.bi_user.uid = jres['id']
        self.bi_user.username = jres['username']
        return True

    def sso_get_userinfo(self):
        """
        查询态势用户登录信息接口
        {
          "platformMg": 0,
          "userId": "1736677153567223809",
          "orgId": 1,
          "realname": "test36",
          "lastLoginIp": null,
          "lastLoginTime": null,
          "phone": "18851656702",
          "originalPlatformMg": 0,
          "tenantId": -1,
          "tenantMg": true,
          "originalTenantId": -1,
          "originalTenantMg": true,
          "pwdExpired": false,
          "email": "113@qq.com",
          "username": "test36"
        }
        """

        url = self.make_url('/maxs/pm/sso/login/getLoginInfo')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res.text}'
        return True

    def sso_get_maxs_org(self):
        """查询态势用户管理组织范围"""
        url = self.make_url(f'/maxs/pm/rpc/_queryOrgList?userId={self.bi_user.uid}')
        res = self.session.post(url)
        assert res.ok, f'接口出错，url：{url}, res: {res.text}'
        return True

    def sso_get_user_org(self):
        """
        BI查询用户信息
        {
          "config": null,
          "createBy": "1736677154959732737",
          "createTime": "2023-12-19 13:56:57",
          "id": "1ab7550051d5441d87855282e93c5608",
          "permission": null,
          "relId": "88d79672963748d98213dac5f776d5fe",
          "relType": "LAST_VISITED_ORGANIZATION",
          "updateBy": null,
          "updateTime": null,
          "userId": "1736677154959732737"
        }
        """

        url = self.make_url(f'/maxs/bi/engine/settings/user')
        res = self.session.get(url).json()
        assert res['success'], f'接口出错，url：{url}, res: {res.text}'
        if not res['data']:
            url = self.make_url(f'/maxs/bi/engine/settings/user')
            data = {
                "relId": "88d79672963748d98213dac5f776d5fe",
                "relType": "LAST_VISITED_ORGANIZATION",
                "config": None
            }
            res = self.session.post(url, json=data).json()
            assert res['success'], f'接口出错，url：{url}, res: {res}'
            org = res['data']['relId']
        else:
            org = res['data'][0]['relId']

        self.bi_user.org = org
        return True

    def sso_create_user(self):
        """BI查询用户信息"""
        url = self.make_url('/maxs/pm/sso/login/_loginexist?random=1702965415562')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res.text}'
        return True


class BiDashboard(BiBase):
    """
    仪表板
    """


class BiChart(BiBase):
    """
    图表
    """

    def chart_list(self):
        """查询数据图表列表接口"""
        url = self.make_url(f'/maxs/bi/engine/bi-viz/pageQueryDatacharts')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "beginTime": None,
            "endTime": None,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        assert res['success'], f'接口出错，url：{url}, res: {res}'

        return True

    def chart_create(self):
        """创建数据图表"""
        url = self.make_url('/maxs/bi/engine/bi-viz/datacharts')
        name = self.random_uname
        data = {
            "name": name,
            "orgId": self.bi_user.org,
            "index": 0,
            "viewId": "b1f701d6497e4347ae2acdffca45b038"  # top10
        }
        create_res = self.session.post(url, json=data).json()
        assert create_res['success'], f'接口出错，url：{url}, res: {create_res}'

        return True

    def chart_update(self):
        """创建数据图表"""
        url = self.make_url(f'/maxs/bi/engine/bi-viz/pageQueryDatacharts')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "beginTime": None,
            "endTime": None,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        chart_id = res['data'][0]['id']
        name = res['data'][0]['name']
        view_id = res['data'][0]['viewId']

        url = self.make_url(f'/maxs/bi/engine/bi-viz/datacharts/{chart_id}')
        data = {
            "id": chart_id,
            "index": 0,
            "parent": 0,
            "name": name,
            "viewId": view_id,
            "config": "{\"aggregation\":true,\"chartConfig\":{\"datas\":[{\"actions\":{\"NUMERIC\":[\"alias\",\"sortable\"],\"STRING\":[\"alias\",\"sortable\",\"topN\"],\"DATE\":[\"alias\",\"sortable\",\"dateLevel\",\"dateFormat\"]},\"label\":\"clusterBarChartDimension\",\"key\":\"dimension\",\"required\":true,\"type\":\"group\",\"limit\":[0,1],\"drillable\":true,\"rows\":[{\"uid\":\"d943db0b-ef4e-4840-94e1-8815841983d6\",\"colName\":\"攻击者IP\",\"type\":\"STRING\",\"subType\":\"UNCATEGORIZED\",\"category\":\"field\",\"children\":[],\"index\":0}]},{\"allowSameField\":true,\"actions\":{\"NUMERIC\":[\"aggregate\",\"alias\",\"format\",\"sortable\",\"colorSingle\",\"topN\"],\"STRING\":[\"aggregateLimit\",\"alias\",\"format\",\"sortable\",\"colorSingle\",\"topN\"]},\"label\":\"clusterBarChartMetrics\",\"key\":\"metrics\",\"required\":true,\"rows\":[{\"uid\":\"a639c7c2-f8a3-466b-b5fe-ad05c0698b54\",\"colName\":\"攻击次数\",\"type\":\"NUMERIC\",\"subType\":\"UNCATEGORIZED\",\"category\":\"field\",\"children\":[],\"aggregate\":\"SUM\"}],\"type\":\"aggregate\",\"limit\":[1,5]}],\"styles\":[{\"label\":\"bar.title\",\"key\":\"bar\",\"comType\":\"group\",\"rows\":[{\"label\":\"common.borderStyle\",\"key\":\"borderStyle\",\"value\":{\"type\":\"solid\",\"width\":0,\"color\":\"#ced4da\"},\"comType\":\"line\",\"rows\":[]},{\"label\":\"bar.radius\",\"key\":\"radius\",\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"bar.width\",\"key\":\"width\",\"value\":36,\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"bar.gap\",\"key\":\"gap\",\"value\":0.1,\"comType\":\"inputPercentage\",\"rows\":[]}]},{\"label\":\"label.title\",\"key\":\"label\",\"comType\":\"group\",\"rows\":[{\"label\":\"label.showLabel\",\"key\":\"showLabel\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"label.position\",\"key\":\"position\",\"value\":\"top\",\"comType\":\"labelPosition\",\"rows\":[]},{\"label\":\"viz.palette.style.font\",\"key\":\"font\",\"value\":{\"fontFamily\":\"PingFang SC\",\"fontSize\":\"12\",\"fontWeight\":\"normal\",\"fontStyle\":\"normal\",\"color\":\"#8A9099\"},\"comType\":\"font\",\"rows\":[]}]},{\"label\":\"legend.title\",\"key\":\"legend\",\"comType\":\"group\",\"rows\":[{\"label\":\"legend.showLegend\",\"key\":\"showLegend\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"legend.type\",\"key\":\"type\",\"value\":\"scroll\",\"comType\":\"legendType\",\"rows\":[]},{\"label\":\"legend.selectAll\",\"key\":\"selectAll\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"legend.position\",\"key\":\"position\",\"value\":\"bottom\",\"comType\":\"legendPosition\",\"rows\":[]},{\"label\":\"legend.height\",\"key\":\"height\",\"value\":0,\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"viz.palette.style.font\",\"key\":\"font\",\"value\":{\"fontFamily\":\"PingFang SC\",\"fontSize\":\"12\",\"fontWeight\":\"normal\",\"fontStyle\":\"normal\",\"color\":\"#8A9099\"},\"comType\":\"font\",\"rows\":[]}]},{\"label\":\"xAxis.title\",\"key\":\"xAxis\",\"comType\":\"group\",\"rows\":[{\"label\":\"common.showAxis\",\"key\":\"showAxis\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.inverseAxis\",\"key\":\"inverseAxis\",\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.lineStyle\",\"key\":\"lineStyle\",\"value\":{\"type\":\"solid\",\"width\":1,\"color\":\"#AEB2B8\"},\"comType\":\"line\",\"rows\":[]},{\"label\":\"common.showLabel\",\"key\":\"showLabel\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"viz.palette.style.font\",\"key\":\"font\",\"value\":{\"fontFamily\":\"PingFang SC\",\"fontSize\":\"12\",\"fontWeight\":\"normal\",\"fontStyle\":\"normal\",\"color\":\"#8A9099\"},\"comType\":\"font\",\"rows\":[]},{\"label\":\"common.rotate\",\"key\":\"rotate\",\"value\":0,\"comType\":\"inputNumber\",\"rows\":[]}]},{\"label\":\"yAxis.title\",\"key\":\"yAxis\",\"comType\":\"group\",\"rows\":[{\"label\":\"common.showAxis\",\"key\":\"showAxis\",\"value\":false,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.inverseAxis\",\"key\":\"inverseAxis\",\"value\":false,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.lineStyle\",\"key\":\"lineStyle\",\"value\":{\"type\":\"solid\",\"width\":1,\"color\":\"#AEB2B8\"},\"comType\":\"line\",\"rows\":[]},{\"label\":\"common.showLabel\",\"key\":\"showLabel\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"viz.palette.style.font\",\"key\":\"font\",\"value\":{\"fontFamily\":\"PingFang SC\",\"fontSize\":\"12\",\"fontWeight\":\"normal\",\"fontStyle\":\"normal\",\"color\":\"#8A9099\"},\"comType\":\"font\",\"rows\":[]},{\"label\":\"common.showTitleAndUnit\",\"key\":\"showTitleAndUnit\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.nameLocation\",\"key\":\"nameLocation\",\"value\":\"center\",\"comType\":\"nameLocation\",\"rows\":[]},{\"label\":\"common.nameRotate\",\"key\":\"nameRotate\",\"value\":90,\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"common.nameGap\",\"key\":\"nameGap\",\"value\":40,\"comType\":\"inputNumber\",\"rows\":[]}]},{\"label\":\"splitLine.title\",\"key\":\"splitLine\",\"comType\":\"group\",\"rows\":[{\"label\":\"splitLine.showHorizonLine\",\"key\":\"showHorizonLine\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.lineStyle\",\"key\":\"horizonLineStyle\",\"value\":{\"type\":\"solid\",\"width\":1,\"color\":\"#E8EAED\"},\"comType\":\"line\",\"rows\":[]},{\"label\":\"splitLine.showVerticalLine\",\"key\":\"showVerticalLine\",\"value\":false,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"common.lineStyle\",\"key\":\"verticalLineStyle\",\"value\":{\"type\":\"solid\",\"width\":1,\"color\":\"#E8EAED\"},\"comType\":\"line\",\"rows\":[]}]},{\"label\":\"viz.palette.style.margin.title\",\"key\":\"margin\",\"comType\":\"group\",\"rows\":[{\"label\":\"viz.palette.style.margin.containLabel\",\"key\":\"containLabel\",\"value\":true,\"comType\":\"checkbox\",\"rows\":[]},{\"label\":\"viz.palette.style.margin.left\",\"key\":\"marginLeft\",\"value\":\"5%\",\"comType\":\"marginWidth\",\"rows\":[]},{\"label\":\"viz.palette.style.margin.right\",\"key\":\"marginRight\",\"value\":\"5%\",\"comType\":\"marginWidth\",\"rows\":[]},{\"label\":\"viz.palette.style.margin.top\",\"key\":\"marginTop\",\"value\":\"7%\",\"comType\":\"marginWidth\",\"rows\":[]},{\"label\":\"viz.palette.style.margin.bottom\",\"key\":\"marginBottom\",\"value\":\"8%\",\"comType\":\"marginWidth\",\"rows\":[]}]}],\"settings\":[{\"label\":\"viz.palette.setting.paging.title\",\"key\":\"paging\",\"comType\":\"group\",\"rows\":[{\"label\":\"viz.palette.setting.paging.pageSize\",\"key\":\"pageSize\",\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"viz.palette.setting.paging.pageSize\",\"key\":\"pageSizeTop\",\"comType\":\"inputNumber\",\"rows\":[]},{\"label\":\"viz.palette.setting.paging.pageSize\",\"key\":\"pageSizeBig\",\"comType\":\"inputNumber\",\"rows\":[]}]},{\"label\":\"reference.title\",\"key\":\"reference\",\"comType\":\"group\",\"rows\":[{\"label\":\"reference.open\",\"key\":\"panel\",\"comType\":\"reference\",\"rows\":[]}]}],\"interactions\":[{\"label\":\"drillThrough.title\",\"key\":\"drillThrough\",\"comType\":\"checkboxModal\",\"rows\":[{\"label\":\"drillThrough.title\",\"key\":\"setting\",\"comType\":\"interaction.drillThrough\",\"rows\":[]}]},{\"label\":\"viewDetail.title\",\"key\":\"viewDetail\",\"comType\":\"checkboxModal\",\"rows\":[{\"label\":\"viewDetail.title\",\"key\":\"setting\",\"comType\":\"interaction.viewDetail\",\"rows\":[]}]}]},\"chartGraphId\":\"cluster-column-chart\",\"computedFields\":[]}",
            "permissions": [],
            "avatar": "cluster-column-chart"
        }
        create_res = self.session.put(url, json=data).json()
        assert create_res['success'], f'接口出错，url：{url}, res: {create_res}'

        return True

    def chart_show(self):
        """查看数据图表"""
        url = self.make_url(f'/maxs/bi/engine/bi-viz/pageQueryDatacharts')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "beginTime": None,
            "endTime": None,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        chart_id = res['data'][0]['id']

        url = self.make_url(f'/maxs/bi/engine/bi-viz/datacharts/{chart_id}')
        create_res = self.session.get(url).json()
        assert create_res['success'], f'接口出错，url：{url}, res: {create_res}'

        return True

    def chart_delete(self):
        """删除数据图表"""
        url = self.make_url(f'/maxs/bi/engine/bi-viz/pageQueryDatacharts')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "beginTime": None,
            "endTime": None,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        chart_id = res['data'][0]['id']

        url = self.make_url(f'/maxs/bi/engine/viz/datacharts/{chart_id}?archive=false')
        create_res = self.session.delete(url).json()
        assert create_res['success'], f'接口出错，url：{url}, res: {create_res}'

        return True


class BiDataset(BiBase):
    """
    数据集
    """

    def ds_list(self):
        """数据集列表查询"""
        url = self.make_url(f'/maxs/bi/engine/bi-views/pageQueryViews')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        assert res['success'], f'接口出错，url：{url}, res: {res}'

        return True

    def ds_create(self):
        """创建数据集"""
        url = self.make_url(f'/maxs/bi/engine/data-provider/execute/test')
        data = {
            "script": "SELECT\n  nested (ATTACKER_INFO.IP) AS 攻击者IP,\n  count(reverse_nested (SNOW_ID)) AS 攻击次数\nFROM\n  maxs_alarm_20*\nGROUP BY\n  nested (ATTACKER_INFO.IP)\nORDER BY\n  攻击次数 DESC\nLIMIT\n  10",
            "sourceId": "82f1976259b14f9daac2c99d76777349",
            "size": 1000,
            "scriptType": "SQL",
            "columns": "",
            "variables": []
        }
        test_res = self.session.post(url, json=data).json()
        assert test_res['success'], f'接口出错，url：{url}, res: {test_res}'

        url = self.make_url(f'/maxs/bi/engine/views/check/name')
        name = self.random_uname
        data = {
            "name": name,
            "orgId": self.bi_user.org,
            "parentId": None
        }
        name_res = self.session.post(url, json=data).json()
        assert name_res['success'], f'接口出错，url：{url}, res: {name_res}'

        url = self.make_url('/maxs/bi/engine/views')
        data = {
            "orgId": self.bi_user.org,
            "name": name,
            "sourceId": "82f1976259b14f9daac2c99d76777349",
            "parentId": None,
            "isFolder": False,
            "index": 121,
            "type": "SQL",
            "script": "SELECT\n  nested (ATTACKER_INFO.IP) AS 攻击者IP,\n  count(reverse_nested (SNOW_ID)) AS 攻击次数\nFROM\n  maxs_alarm_20*\nGROUP BY\n  nested (ATTACKER_INFO.IP)\nORDER BY\n  攻击次数 DESC\nLIMIT\n  10",
            "config": "{\"version\":\"1.0.0-RC.2\",\"concurrencyControl\":true,\"concurrencyControlMode\":\"DIRTYREAD\",\"cache\":false,\"cacheExpires\":0}",
            "model": "{\"version\":\"1.0.0-RC.2\",\"columns\":{\"攻击者IP\":{\"name\":\"攻击者IP\",\"type\":\"STRING\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击者IP\"]},\"攻击次数\":{\"name\":\"攻击次数\",\"type\":\"NUMERIC\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击次数\"]}},\"hierarchy\":{\"攻击者IP\":{\"name\":\"攻击者IP\",\"type\":\"STRING\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击者IP\"]},\"攻击次数\":{\"name\":\"攻击次数\",\"type\":\"NUMERIC\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击次数\"]}}}",
            "variablesToCreate": [],
            "columnPermission": []
        }
        create_res = self.session.post(url, json=data).json()
        assert create_res['success'], f'接口出错，url：{url}, res: {create_res}'
        return True

    def ds_update(self):
        """编辑数据集"""
        url = self.make_url(f'/maxs/bi/engine/bi-views/pageQueryViews')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        assert res['success'], f'接口出错，url：{url}, res: {res}'

        rid = res['data'][0]['id']
        name = res['data'][0]['name']
        url = self.make_url(f'/maxs/bi/engine/views/{rid}')
        data = {
            "orgId": self.bi_user.org,
            "name": name,
            "sourceId": "82f1976259b14f9daac2c99d76777349",
            "isFolder": False,
            "index": 121,
            "type": "SQL",
            "script": "SELECT\n  nested (ATTACKER_INFO.IP) AS 攻击者地址,\n  count(reverse_nested (SNOW_ID)) AS 攻击次数\nFROM\n  maxs_alarm_20*\nGROUP BY\n  nested (ATTACKER_INFO.IP)\nORDER BY\n  攻击次数 DESC\nLIMIT\n  10",
            "config": "{\"version\":\"1.0.0-RC.2\",\"concurrencyControl\":true,\"concurrencyControlMode\":\"DIRTYREAD\",\"cache\":false,\"cacheExpires\":0}",
            "model": "{\"version\":\"1.0.0-beta.4\",\"columns\":{\"攻击者地址\":{\"name\":\"攻击者地址\",\"type\":\"STRING\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击者地址\"]},\"攻击次数\":{\"name\":[\"攻击次数\"],\"type\":\"NUMERIC\",\"category\":\"UNCATEGORIZED\"}},\"hierarchy\":{\"攻击者地址\":{\"name\":\"攻击者地址\",\"type\":\"STRING\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击者地址\"]},\"攻击次数\":{\"name\":\"攻击次数\",\"type\":\"NUMERIC\",\"category\":\"UNCATEGORIZED\",\"path\":[\"攻击次数\"]}}}",
        }
        res = self.session.put(url, json=data).json()
        assert res['success'], f'接口出错，url：{url}, res: {res}'

        return True

    def ds_delete(self):
        """删除数据集"""
        url = self.make_url(f'/maxs/bi/engine/bi-views/pageQueryViews')
        data = {
            "pageSize": 10,
            "pageNo": 1,
            "orgId": self.bi_user.org
        }
        res = self.session.post(url, json=data).json()
        assert res['success'], f'接口出错，url：{url}, res: {res}'
        rid = res['data'][0]['id']

        url = self.make_url(f'/maxs/bi/engine/views/{rid}?archive=true')
        name_res = self.session.delete(url).json()
        assert name_res['success'], f'接口出错，url：{url}, res: {name_res}'

        return True


class BiHandler(BiDashboard,
                BiChart,
                BiDataset,
                BiSso,
                ):
    """
    智能报表
    """
