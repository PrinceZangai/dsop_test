import hashlib
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher, PKCS1_OAEP
import requests
import logging
from robot.api.deco import keyword

class Crypto:
#     public_key="""-----BEGIN PUBLIC KEY-----
# MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCkvEUyoCqPdpWuz8qGiI3waEYkc6IGMf44X9/RTs1lgl6OG1eJB2b+78fnRfvkhPC5Xt/6YnZDJ4KAiokmQgj+FW/Fw93DmDWkxcozUIFcOPhc1Oa93Bdze4yVObux+xMCgdTWNMbsicqXtTRkqVFYRIKMHTAjJfn33J+Lm5IWJwIDAQAB
# -----END PUBLIC KEY-----"""
#     private_key="""-----BEGIN PRIVATE KEY-----
# MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY
# 7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKN
# PuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gA
# kM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWow
# cSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99Ecv
# DQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthh
# YhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3
# UP8iWi1Qw0Y=
# -----END PRIVATE KEY-----"""

    # def encrypto(self,message):

    #     pub_key = RSA.importKey(Crypto.public_key)
    #     cipher = PKCS1_cipher.new(pub_key)
    #     rsa_text = base64.b64encode(cipher.encrypt(message.encode("utf-8)")))  # 加密并转为b64编码
    #     text = rsa_text.decode("utf8")
    #     return text
    
    def handle_key(self,key,type=None):
        """
        处理公钥格式
        :param pub_key:
        :return:
        """
        if type=="pub":
            start = '-----BEGIN PUBLIC KEY-----\n'
            end = '-----END PUBLIC KEY-----'
        else:
            start = '-----BEGIN PRIVATE KEY-----\n'
            end = '-----END PRIVATE KEY-----'
        result = ''
        # 分割key，每64位长度换一行
        length = len(key)
        divide = 64  # 切片长度
        offset = 0  # 拼接长度
        while length - offset > 0:
            if length - offset > divide:
                result += key[offset:offset + divide] + '\n'
            else:
                result += key[offset:] + '\n'
            offset += divide
        result = start + result + end
        return result

    @keyword("加密")
    def encrypt(self,public_key,password):
        rsakey = RSA.importKey(public_key)
        cipher = PKCS1_cipher.new(rsakey)
        cipher_text =base64.b64encode(cipher.encrypt(password.encode("utf-8")))
        return cipher_text.decode("utf8")

    @keyword("解密")
    def decrypt(self,private_key,ciphertext):
        private_key = RSA.importKey(private_key)
        cipher = PKCS1_cipher.new(private_key)
        plaintext = cipher.decrypt(ciphertext,None)
        print(plaintext)

class Requests:
    @keyword("通用请求")
    def my_request(self,url,method,**kwarg):
        """分装通用请求方法
        |Examples:
            get请求-params参数
            ${resp}    通用请求    www.baidu.com   Get    params=${params}
            post请求-json参数
            ${resp}     通用请求    www.baidu.com   POST   json=${json}
            post请求-data参数
            ${resp}     通用请求    www.baidu.com   POST   data=${data}
            post请求-file参数
            ${resp}     通用请求    www.baidu.com   POST   file=${file}
            delete请求
            ${resp}     通用请求    www.baidu.com   POST   DELETE=${data}
        |Args:
            url (_type_): 请求url
            method (_type_): 请求方法
            kwarg: 请求参数，json、data、file、params、headers等等，详情参考
        |Raises:
            ValueError: _description_

        |Returns:
            _type_: response
        """
        assert isinstance(method,str)
        if method.lower()=="get":
            resp=requests.get(url,verify=False,**kwarg)
        elif method.lower()=="post":
            resp=requests.post(url,verify=False,**kwarg)
        elif method.lower()=="delete":
            resp=requests.delete(url,verify=False,**kwarg)
        elif method.lower()=="put":
            resp=requests.put(url,verify=False,**kwarg)
        else:
            raise ValueError("方法不允许")
        logging.info(f"{resp.request.method} Request : {resp.request.url}\nheaders={resp.request.headers}\nbody={resp.request.body}")
        logging.info(f"{resp.request.method} Response : {resp.request.url}\nheaders={resp.headers}\nbody={resp.content}")
        return resp

if __name__=="__main__":
    crypto=Crypto()
    encrypt_password = crypto.encrypt('123456')
    decrypt_password = crypto.decrypt(encrypt_password)

    print(encrypt_password)
    # 生成 RSA 密钥对
    key = RSA.generate(2048)

    # 获取公钥和私钥
    public_key = key.publickey()
    private_key = key

    # public_key=RSA.import_key(crypto.public_key)
    # private_key=RSA.import_key(crypto.private_key)
    # # 加密
    # plaintext = b"Hello, World!"
    # cipher = PKCS1_cipher.new(public_key)
    # ciphertext = cipher.encrypt(plaintext)
    # print(f"Ciphertext: {ciphertext.hex()}")

    # # 解密
    # cipher = PKCS1_cipher.new(private_key)
    # decrypted_text = cipher.decrypt(ciphertext, None)
    # print(f"Decrypted Text: {decrypted_text.decode('utf-8')}")