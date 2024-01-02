import re

from requests import Session

from ..base import make_url
from ..h2 import H2Connector


class ClusterBaseHandler:
    def __init__(self, domain, user, pwd):
        self.domain = domain
        self.user = user
        self.pwd = pwd
        self.session = Session()
        self.session.verify = False
        self.cancel_captcha()
        self.login()

    def cancel_captcha(self):
        """取消验证码"""
        ip = re.search('http://(.*?):\d+/', self.domain).group(1)
        ins = H2Connector(ip, '8082', 'root', 'maxs.PDG~2022', 'CLUSTER')
        sql = """insert into  CLUSTER_CONFIG_INFO (CODE, NAME, CREATE_TIME) values ('CAPTCHA_SWITCH', 1, now());"""
        ins.execute(sql)

    def make_url(self, url):
        return make_url(self.domain, url)

    def login(self):
        url = self.make_url('/clusterOps/loginManager/login')
        data = {
            "uuid": "captcha_10",
            "username": self.user,
            "password": self.pwd,
            "code": "1234"
        }
        res = self.session.post(url, json=data)
        jres = res.json()
        if jres['message'] != 'success':
            raise Exception(f'登录失败.data:{data},res:{jres}')
        self.session.cookies = res.cookies
        return res
