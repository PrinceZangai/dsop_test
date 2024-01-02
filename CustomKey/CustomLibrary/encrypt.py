import base64

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA


class Encryptor:
    """
    加密类
    """
    @staticmethod
    def pwd_encrypt(pwd='123456'):
        """
        密码加密
        """
        public_key = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQChDnCJSDnLdKrK5QBv7hb+QNIWiC2slLOeWYUQ" + \
                     "hA7DKYKp7f6aKmWFE7mDRnA/LUoo26yxEJcfT9Wt2CzMmrjnRQDT3BmJxlWBHul90Hv1dMVdkrDn" + \
                     "+dP7uXLLeiT4NFwbhLRMVYrMaXSdRDaRAG6g6oDIJfPM24XvBVZf3a/J7wIDAQAB"  # 输入对应的公钥
        key = '-----BEGIN PUBLIC KEY-----\n' + public_key + '\n-----END PUBLIC KEY-----'
        rsakey = RSA.importKey(key)  # 读取公钥
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        # 因为encryptor.encrypt方法其内部就实现了加密再次Base64加密的过程，所以这里实际是通过下面的1和2完成了JSEncrypt的加密方法
        encrypt_text = cipher.encrypt(pwd.encode())  # 1.对账号密码组成的字符串加密
        cipher_text_tmp = base64.b64encode(encrypt_text)  # 2.对加密后的字符串base64加密
        return cipher_text_tmp.decode()
