import json
import os
import random
import re
import time

from requests.sessions import Session
from requests_toolbelt import MultipartEncoder

from .base import make_url, generate_random_word, get_time_ranges, TIME_FORMAT_1
from .connector import SocketConnector


class BaseHandler:

    def __init__(self, domain, cookies, master=None, context=None):
        """
        :param url: 平台地址
        :param redis_host: redis地址
        :param user: 登录账号
        :param pwd: 登录密码
        """
        self.domain = domain
        self.master = master or re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.domain).group(0)
        self.context = context or {}
        if isinstance(self.context, str):
            self.context = json.loads(self.context)

        self.session = Session()
        self.session.verify = False
        self.cache = dict()
        if isinstance(cookies, str):
            self.session.headers.update({'cookie': cookies})
        else:
            self.session.cookies = cookies

        self.prepare_data()

    def make_url(self, url):
        return make_url(self.domain, url)

    def prepare_data(self):
        pass

    @property
    def has_license(self):
        cache_k = 'has_license'
        cache_v = self.cache.get(cache_k)
        if cache_v is not None:
            return cache_v

        url = self.make_url('/maxs/pm/system/license/queryLic.do')
        res = self.session.get(url).json()
        ai_license = list(filter(lambda x: x['featureCode'] == 'N5G4', res['data']))

        result = False
        if ai_license and ai_license[0]['licStatus'] == 'effective':
            result = True

        self.cache.update({cache_k: result})
        return result

    @property
    def random_uname(self):
        names = ["Emma",
                 "Olivia",
                 "Ava",
                 "Isabella",
                 "Sophia",
                 "Mia",
                 "Charlotte",
                 "Amelia",
                 "Harper",
                 "Evelyn",
                 "Abigail",
                 "Emily",
                 "Elizabeth",
                 "Sofia",
                 "Avery",
                 "Ella",
                 "Scarlett",
                 "Grace",
                 "Chloe",
                 "Victoria"]

        return random.choice(names) + " " + generate_random_word(5)

    def get_users(self, query: dict = None):
        """
        {
                "userId": "1733046250938249217",
                "name": "jwtest",
                "username": "jwtest",
                "status": 1,
                "phone": "17821901221",
                "email": "test@123.com",
                "dd": "",
                "wchat": "",
                "gender": 1,
                "photo": null,
                "personType": null,
                "userType": 1,
                "workExperience": null,
                "lockedTime": null,
                "errorTimes": 0,
                "pwdModifyTime": "2023-12-08 17:04:14",
                "tenantId": -1,
                "areaId": null,
                "roleIds": "-2",
                "orgIds": "1",
                "orgNames": "默认租户总部",
                "avatar": null,
                "publicKey": null,
                "privateKey": null,
                "createTime": "2023-12-08 16:49:59"
            }
        :param query:
        :return:
        """
        url = self.make_url('/maxs/pm/user/userCfg/pageMaxsUser')
        query = query or dict()
        data = {
            "pageSize": 10,
            "pageIndex": 1,
            "name": "",
            "username": ""
        }
        data.update(query)
        res = self.session.post(url, json=data).json()
        return res['data']['rowData']

    def get_user_ids(self):
        row_data = self.get_users()
        return [i['userId'] for i in row_data]

    def get_roles(self, query: dict = None):
        url = self.make_url('/maxs/pm/messageRule/getUserCountByRole')
        query = query or dict()
        data = {
            "roleName": "",
            "pageIndex": 1,
            "pageSize": 10
        }
        data.update(query)
        res = self.session.post(url, json=data).json()
        return res['data']['rowData']

    def get_role_ids(self):
        row_data = self.get_roles()
        return [i['roleId'] for i in row_data]

    def get_org_tree(self):
        url = self.make_url('/maxs/rv/pa/preAlarm/getOrgTree')
        res = self.session.post(url).json()
        return res['data']

    @staticmethod
    def encode_file(file, field_name='file', data: dict = None):
        """
        把文件转码为文件传输的格式，返回data和headers
        """
        f = open(file, 'rb')
        data = data or {}
        fields = {field_name: (file, f.read(), 'application/octet-stream')}
        fields.update(data)
        f.close()
        encoder = MultipartEncoder(fields=fields)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': encoder.content_type
        }
        return encoder, headers


handler_cache = dict()


class BaseProxy:
    def get_handler(self, cls, *args, **kwargs):
        if handler_cache.get(cls.__name__) is None:
            ins = cls(*args, **kwargs)
            handler_cache.update({cls.__name__: ins})

        return handler_cache.get(cls.__name__)


class BaseAlarmHandler(BaseHandler):
    log_file = os.path.join('Web服务器遭受大规模网络攻击', 'tda.log')

    def make_warns(self):
        # 发送日志
        log_file = os.path.join(os.path.dirname(__file__), 'logs', self.log_file)
        conn = SocketConnector(self.master, port=8805)
        # for _ in range(1000):
        conn.send_log(log_file, False)

        conn.close()

        # 轮训等待告警产生
        for _ in range(300):
            res = self.get_warns()
            warns = res['data']['rowData']
            if warns:
                break

            time.sleep(10)
        else:
            raise Exception("此环境5分钟内未产生告警")

    def get_warns(self, page=1, page_size=10, query: dict = None) -> dict:
        """获取告警列表"""
        url = self.make_url('/maxs/rv/alarm/pageAlarm')
        time_range = get_time_ranges(TIME_FORMAT_1)
        start, end = time_range['最近7天']
        payload = {
            "pageIndex": page,
            "pageSize": page_size,
            "startTime": start,
            "endTime": end,
        }
        query = query or {}
        payload.update(query)
        res = self.session.post(url=url, json=payload)
        j_res = res.json()
        return j_res
