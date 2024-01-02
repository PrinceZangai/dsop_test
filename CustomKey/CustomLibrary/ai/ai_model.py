import random

from .ai_base import AiBaseHandler
from ..base import get_time_days_ago, get_ctime_str, get_now
from ..base import no_license_pass, pass_unittest


class AiModelHandler(AiBaseHandler):
    """
    AI降噪-模型
    """

    @no_license_pass(True)
    def test_list(self):
        """获取模型列表"""
        url = self.make_url('/maxs/sdb/model/list')
        query = {
            "modelName": "",
            "status": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(url, json=query).json()
        assert res['code'] == 200
        assert isinstance(res['data']['records'], list)

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_detail(self):
        """模型详情"""
        list_url = self.make_url('/maxs/sdb/model/list')
        query = {
            "modelName": "",
            "status": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(list_url, json=query).json()
        assert len(res['data']['records']) > 0, "此环境没有AI模型"

        model_id = res['data']['records'][-1]['taskId']
        detail_url = self.make_url(f'/maxs/sdb/model/detail/{model_id}')
        res = self.session.get(detail_url).json()
        assert res['code'] == 200, "模型详情接口错误"

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_detail_statistics(self):
        """模型详情统计数据"""
        list_url = self.make_url('/maxs/sdb/model/list')
        query = {
            "modelName": "",
            "status": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(list_url, json=query).json()
        assert len(res['data']['records']) > 0, "此环境没有AI模型"

        model_id = res['data']['records'][-1]['taskId']
        detail_url = self.make_url(f'/maxs/sdb/model/getModelStatistics/{model_id}')
        res = self.session.get(detail_url).json()
        assert res['code'] == 200, "模型详情统计接口错误"

        fields = list(res['data'].keys())
        expect_fields = ['alarmNum', 'errNum', 'noiseNum', 'totalNum', 'totalTime']
        assert sorted(fields) == sorted(expect_fields), f'返回字段不符合期望，返回：{fields}，期望：{expect_fields}'

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_rename(self):
        """模型更名"""
        list_url = self.make_url('/maxs/sdb/model/list')
        query = {
            "modelName": "",
            "status": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(list_url, json=query).json()
        assert len(res['data']['records']) > 0, "此环境没有AI模型"

        unused_models = [i for i in res['data']['records'] if i['use'] == 0]
        model = unused_models[-1]
        model_id = model['taskId']

        uid = random.random()
        new_name = f'test_rename_{uid}'

        rename_url = self.make_url(f'/maxs/sdb/model/updateModelName/{model_id}?modelName={new_name}')
        res = self.session.get(rename_url).json()
        assert res['code'] == 200, f'改名失败,msg:{res["message"]}'

        name_query = {
            "modelName": new_name,
            "status": model['status'],
            "pageIndex": 1,
            "pageSize": 10,
            'endTime': model['finishTime'],
            'startTime': model['startTime']
        }
        res: dict = self.session.post(list_url, json=name_query).json()
        assert len(res['data']['records']) == 1, '改名后模型列表没有搜索到此名称'

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_manual_train(self):
        """手动训练"""
        url = self.make_url('/maxs/sdb/model/train')
        end_time = get_ctime_str()
        now = get_now()
        start_time = get_time_days_ago(now, 7)
        data = {'startDate': start_time, 'endData': end_time}
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'手动训练模型接口出错, msg:{res["message"]}'
        model_name = res['message']

        list_url = self.make_url('/maxs/sdb/model/list')
        name_query = {
            "modelName": model_name,
            "status": 0,
            "pageIndex": 1,
            "pageSize": 10,
        }
        res: dict = self.session.post(list_url, json=name_query).json()
        assert len(res['data']['records']) == 1, '手动训练后模型列表没有搜索到新模型'

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_enable_model(self):
        """启用模型"""

        list_url = self.make_url('/maxs/sdb/model/list')
        query = {
            "status": 2,
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(list_url, json=query).json()
        assert len(res['data']['records']) > 0, "此环境没有训练成功的AI模型"

        unused_models = [i for i in res['data']['records'] if i['use'] == 0]
        assert len(unused_models) > 0, '此环境没有训练成功且未使用的模型'

        model = random.choice(unused_models)
        model_id = model['taskId']

        url = self.make_url(f'/maxs/sdb/model/apply/{model_id}')
        res = self.session.get(url).json()
        assert res['code'] == 200

        return True

    @pass_unittest(True)
    @no_license_pass(True)
    def test_delete_model(self):
        """删除模型"""
        list_url = self.make_url('/maxs/sdb/model/list')
        query = {
            "status": 3,
            "pageIndex": 1,
            "pageSize": 10
        }
        res: dict = self.session.post(list_url, json=query).json()
        assert len(res['data']['records']) > 0, "此环境没有训练失败的AI模型"

        model = random.choice(res['data']['records'])
        model_id = model['taskId']
        url = self.make_url(f'/maxs/sdb/model/delete/{model_id}')
        res = self.session.get(url).json()
        assert res['code'] == 200, '删除模型接口出错'

        return True
