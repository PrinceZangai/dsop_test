import requests

from .base import make_url
from .captcha import Captcha
from .encrypt import Encryptor


class MaxsLogin:
    @staticmethod
    def get_login_cookies(url, host, user, pwd):
        session = requests.session()
        if len(pwd) < 30:
            pwd = Encryptor.pwd_encrypt(pwd)

        c_handler = Captcha(url, host)
        uuid = c_handler.get_captcha_uuid()
        captcha = c_handler.get_captcha_key(uuid)
        data = {"username": user,
                "password": pwd,
                "captcha": captcha,
                "captchaUuid": uuid,
                "tenantId": -1}
        url = make_url(url, '/maxs/pm/sso/login/_login')
        res = session.post(url, json=data, timeout=5, verify=False)
        if "登录成功" not in res.text:
            raise Exception(f"登录失败.response:{res.text}")

        return res.cookies
        # return """ssa_jwt=eyJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE3MDI5NjYxMTAsImp0aSI6IjE3MzY5OTE4Nzk2ODkzMjY1OTQiLCJ0b2tlblRpbWVvdXQiOjE4MDAsInR5cGUiOiJicm93c2VyIiwic3ViIjoiMTczNjY3NzE1NTQwNDMyODk2MiIsInBsYXRmb3JtTWciOjAsInRlbmFudElkIjotMSwidXNlcm5hbWUiOiJ0ZXN0NDAiLCJuYW1lIjoidGVzdDQwIiwidXNlcl90eXBlIjoxfQ.DvtU84-8E3dW0Tjpoi0QjM8jdpUXDOan-h05I7F655QBHvCbu1_QExdAjRUJan0-4pBHfhYwAUnTVwvVVCMKlUctwK8QicPFvKE4Bk9RFCnQTvw38z8JYz0DZRBp4KYii54WR99Cv2EajQrliI3dkT2rO6RkTOnuICWIkI3_nQFSuJtSLNe474-IYmgTdH7__FEbPXd7G1UJlTbdoHccC45vPxN1WwjdzuAF8-rYtyATtoLgT-VS4v5w19b3GIAE0-OnDruuoA4q30kTabUVlmPQGckW4kob2fGqoh0aMrGq9eo2Hv1TfoTgpE0gCQuUdId1n-0SGR1Jq-xDNM4XCw; AUTHORIZATION_TOKEN=Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0NDAiLCJwYXNzd29yZCI6NDU5NzgwMzM5LCJleHAiOjE3MDI5NzAxODV9.a--IkFMtlkc6kP78STAkIJgqokWvrGaiFIHeDtITDrw"""

