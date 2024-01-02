import warnings

import redis
import requests

from .base import make_url

warnings.filterwarnings('ignore')


class Captcha:
    """
    平台登录验证码相关处理
    """

    def __init__(self, platform_url, redis_host):
        self.url = platform_url
        self.redis_host = redis_host
        self.get_captcha_url = "/maxs/pm/sso/login/_getCaptcha"  # 获取验证码id--URL

    def is_open(self) -> bool:
        """
        判断平台是否启用验证码
        @return:
        """
        url = make_url(self.url, "maxs/pm/sso/login/_isCaptcha")
        res = requests.post(url, verify=False)
        res_data = res.json()
        print(res_data)
        return res_data.get('data', True)

    def get_captcha_uuid(self):
        """
        获取验证码uuid
        """
        if not self.is_open():
            return ''

        url = make_url(self.url, "/maxs/pm/sso/login/_getCaptcha")
        res = requests.post(url, verify=False)
        res_data = res.json()
        uuid = res_data["data"]["captchaUuid"]
        return uuid

    def get_captcha_key(self, captchaUuid):
        '''
        获取验证码

        :param redis_host: 必填，Redis主机
        :param captchaUuid: 必填，从Redis主机中用uuid获取验证码
        '''
        if captchaUuid == '':
            return ''

        r = redis.Redis(host=self.redis_host, port='16379', db=2, password='!QAZxsw2#EDC(0Ol1)')
        captcha = r.get(captchaUuid)  # 返回如b'csck'
        captcha1 = str(captcha)
        captcha_string = captcha1[2:-1]
        return captcha_string


class CaptchaProxy:
    def get_captcha_handler(self, *args, **kwargs):
        return Captcha(*args, **kwargs)


if __name__ == '__main__':
    def linjie_cookie(URL, data):
        # 拼接URL
        is_login_url = URL + '/maxs/pm/sso/login/_login'
        # 发送请求
        reps = requests.post(is_login_url, json=data, verify=False)
        print(reps.json())
        cookie = reps.cookies
        return cookie


    # 定义URL
    Host_URL = 'https://192.168.111.158:8686'
    # 定义redis_host
    Host_redis = '192.168.111.158'

    cap_class = Captcha(Host_URL, Host_redis)
    print(cap_class.is_open())
    cap_tuple = cap_class.get_captcha_uuid(Host_URL)  # 本来是一个元组 print(cap_tuple[0])
    cap_tuple2 = cap_class.get_captcha_key(Host_redis, cap_tuple)
    pwd_encrypt = 'DhXep2JfEWxWt9km9S69oPmCR525xvfb/86ecUXH0JnwdLf+rmqZJnwAQlx0iJczYf8NF2ioyaUWdcHToRBT4iXScaOi0fe5ldwqi/6PDuV7flyCM5Xxjz8SifT/lbDU+O4OK2WeyqPsN1dTpfIwQxUR8/gkhf6jxJzHfaARXDA='
    print(pwd_encrypt)
    data = {"username": "test36",
            "password": pwd_encrypt,
            "captcha": cap_tuple2,
            "captchaUuid": cap_tuple,
            "tenantId": -1}
    print(data)
    print(linjie_cookie(Host_URL, data))
    if_captcha_value=if_captcha(Host_URL,Host_redis)
    if if_captcha_value=='':
        print()#直接执行登录方法吧，嘻嘻
    else:
        Captcha=(get_captcha(Host_redis,if_captcha_value)) #执行连接方法
    # 然后执行登录方法吧，嘻嘻

        cookie=a.get_login_cookies('https://10.21.18.166:8686','/sso/login/_login','{"username":"admin", "password":"H+jOOxq3q6vb6XPUgaUx4Th0jq/5s+I7QDlUEZXcgev1qH5OE0Marc4O1UzSaf3DljMQNuMv3+rZOsMnVyxpo/dPGXr5X4wQGpe+Tb9YAy0hLtx4/S8zqet84xJ74ri15DKcrbAmJofX2TnDEitXukEqoVVmK6phrIEIC2SFiUA=","captcha":"","captchaUuid":"","tenantId":-1}')
