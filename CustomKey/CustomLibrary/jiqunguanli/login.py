from .base import ClusterBaseHandler


class ClusterLogin(ClusterBaseHandler):
    def get_captcha(self):
        """验证码"""
        url = self.make_url(f'/clusterOps/loginManager/verify')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def test_login(self, user, pwd):
        """登录接口"""
        url = self.make_url('/clusterOps/loginManager/login')
        data = {
            "uuid": "captcha_10",
            "username": user,
            "password": pwd,
            "code": "1234"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def test_logout(self):
        """退出接口"""
        url = self.make_url(f'/clusterOps/loginManager/logout')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        self.login()
        return True