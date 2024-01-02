from .ai_base import AiBaseHandler
from ..base import no_license_pass


class AiCfgHandler(AiBaseHandler):
    """
    AI降噪配置
    """

    @no_license_pass(True)
    def test_get_config(self):
        """测试获取降噪配置"""
        url = self.make_url('/maxs/sdb/cfg/getCfg')
        res = self.session.get(url).json()
        return res.get('code') == 200

    @no_license_pass(True)
    def test_set_config_open_ai(self):
        """测试开启智能降噪"""
        url = self.make_url('/maxs/sdb/cfg/setCfg')
        data = {"evolution": 1, "evolutionCondition": 0, "handleDuration": 10, "label": 1, "sampleTriggerNumber": 20000,
                "sdb": 1, "strategy": 1, "strategyType": 1, "score": 0.5}
        res = self.session.post(url, json=data).json()
        return res.get('code') == 200

    @no_license_pass(True)
    def test_set_config_close_ai(self):
        """测试关闭智能降噪"""
        url = self.make_url('/maxs/sdb/cfg/setCfg')
        data = {"evolution": 1, "evolutionCondition": 0, "handleDuration": 10, "label": 1, "sampleTriggerNumber": 20000,
                "sdb": 0, "strategy": 1, "strategyType": 1, "score": 0.5}
        res = self.session.post(url, json=data).json()
        return res.get('code') == 200

    @no_license_pass(True)
    def test_set_config_boundary(self):
        """测试智能降噪配置接口边界值"""
        url = self.make_url('/maxs/sdb/cfg/setCfg')
        # 1. sdb not in [0,1]
        base_data = {
            "evolution": 1,
            "evolutionCondition": 0,
            "handleDuration": 10,
            "label": 1,
            "sampleTriggerNumber": 20000,
            "sdb": 1,
            "strategy": 1,
            "strategyType": 1,
            "score": 0.5
        }
        data = base_data.copy()
        data.update(sdb=2)

        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '是否开启智能降噪只能是0或者1'

        # 2. label not in [0,1]
        data = base_data.copy()
        data.update(label=2)

        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '是否开启告警处置智能标注只能是0或者1'

        # 3. evolution not in [0,1]
        data = base_data.copy()
        data.update(evolution=2)

        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '是否开启智能降噪模型自动进化只能是0或者1'

        # 4. evolutionCondition not in [0,1,2,3]
        data = base_data.copy()
        data.update(evolutionCondition=0)

        res = self.session.post(url, json=data).json()
        assert res.get('code') == 200

        data.update(evolutionCondition=1)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 200

        data.update(evolutionCondition=2)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 200

        data.update(evolutionCondition=3)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 200

        data.update(evolutionCondition=4)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '进化效果判断条件只能是0、1、2或者3'

        # 5. strategy not in [0,1]
        data = base_data.copy()
        data.update(strategy=2)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '是否开启自动样本策略只能是0或者1'

        # 6. strategyType not in [0,1]
        data = base_data.copy()
        data.update(strategyType=2)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '自动触发策略只能是0或者1'

        # 7. sampleTriggerNumber传0，-1
        data = base_data.copy()
        data.update(sampleTriggerNumber=-1)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '自动样本触发条数区间为20000~2147483647的整数'

        # 8. handleDuration传0，-1
        data = base_data.copy()
        data.update(handleDuration='0')
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '自动样本策略周期为1~30的整数'

        data = base_data.copy()
        data.update(handleDuration='-1')
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '自动样本策略周期为1~30的整数'

        data = base_data.copy()
        data.update(handleDuration='31')
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '自动样本策略周期为1~30的整数'

        data = base_data.copy()
        data.update(score=-1)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '告警置信度只能在0-1之间'

        data = base_data.copy()
        data.update(score=1.01)
        res = self.session.post(url, json=data).json()
        assert res.get('code') == 500
        assert res.get('message') == '告警置信度只能在0-1之间'

        return True

    @no_license_pass(True)
    def test_open_auto_mark(self):
        """开启告警处置智能标注"""
        url = self.make_url('/maxs/sdb/cfg/setLabel')
        data = {'label': 1}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'开启告警处置智能标注失败，msg:{res["message"]}'

        return True

    @no_license_pass(True)
    def test_close_auto_mark(self):
        """开启告警处置智能标注"""
        url = self.make_url('/maxs/sdb/cfg/setLabel')
        data = {'label': 0}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'开启告警处置智能标注失败，msg:{res["message"]}'

        return True

    @no_license_pass(True)
    def test_close_auto_mark_boundary(self):
        """开启告警处置智能标注"""
        url = self.make_url('/maxs/sdb/cfg/setLabel')
        data = {'label': 2}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 500
        assert res['message'] == '是否开启告警处置智能标注只能是0或者1'

        return True
