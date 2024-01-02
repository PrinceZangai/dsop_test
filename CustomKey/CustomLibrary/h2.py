import re

import requests

s = requests.Session()


class H2Connector:
    def __init__(self, ip, port, user, pwd, db):
        self.session = requests.Session()
        self.ip = ip
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.domain = f'http://{self.ip}:{self.port}'
        self.sid = self.login()

    def login(self):
        url = f'{self.domain}/'
        res = self.session.get(url)
        sid = re.search('jsessionid=(\w+)', res.text).group(1)

        login_url = f'{self.domain}/login.do'

        param = {'jsessionid': sid}
        data = {
            'language': 'en',
            'setting': 'Generic H2 (Embedded)',
            'name': 'Generic H2 (Embedded)',
            'driver': 'org.h2.Driver',
            'url': f'jdbc:h2:./{self.db}',
            'user': self.user,
            'password': self.pwd

        }
        res = self.session.post(login_url, params=param, data=data)
        if res.ok:
            return sid

    def execute(self, sql):
        url = f'{self.domain}/query.do?jsessionid={self.sid}'
        data = {'sql': sql}
        res = self.session.post(url, data=data)
        return res.text


if __name__ == '__main__':
    ins = H2Connector('192.168.112.123', '8082', 'root', 'maxs.PDG~2022', 'CLUSTER')
    sql = """ insert into  CLUSTER_CONFIG_INFO (CODE, NAME, CREATE_TIME) values ('CAPTCHA_SWITCH', 1, now());"""
    ins.execute(sql)

