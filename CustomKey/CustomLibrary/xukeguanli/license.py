import os

from requests_toolbelt import MultipartEncoder

from ..baseclass import BaseHandler


class LicenseHandler(BaseHandler):
    """
    工单管理
    """

    def lic_query(self):
        """查询系统许可状态"""
        url = self.make_url(f'/maxs/pm/system/license/queryLicense.do')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        return True

    def lic_check(self):
        """查询单个许可状态"""
        url = self.make_url(f'/maxs/pm/system/license/queryLicense.do')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        pid = res['data']['child'][0]['pid']

        url = self.make_url(f'/maxs/pm/system/license/checkLicStatus.do?pid={pid}')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def lic_active(self):
        """查询激活状态"""
        url = self.make_url(f'/maxs/pm/system/license/getActivationInfo.do')
        res = self.session.get(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        return True

    def lic_delete(self):
        """删除许可"""
        pid = 'NAZ00'
        url = self.make_url(f'/maxs/pm/system/license/deleteLicense.do?pid={pid}')
        res = self.session.get(url).json()
        assert res['message'] == 'PID不正确', f'接口出错，url：{url}, res: {res}'

        return True

    def lic_upload(self):
        """上传许可"""
        url = self.make_url(f'/maxs/pm/system/license/uploadLicense.do')
        file = os.path.join(os.path.dirname(__file__), '2611-1.dat')
        f = open(file, 'rb')
        fields = {'file': (file, f.read(), 'application/octet-stream')}
        f.close()
        multipartEncoder = MultipartEncoder(fields=fields)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': multipartEncoder.content_type
        }
        res = self.session.post(url, data=multipartEncoder, headers=headers).json()
        f.close()
        assert res['code'] == 500, f'接口出错，url：{url}, res: {res}'

        return True
