# -*-coding: utf-8 -*-
import warnings

import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

warnings.filterwarnings('ignore')


class HttpFunction():
    def __init__(self):
        self.headers = {
            'Accept': 'application/json;charset=UTF-8, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,und;q=0.6,mt;q=0.5',
            'Content-Type': 'application/json',
            'regionId': 'regi_default'
        }

    def http_get(self, url, path, cookies='', timeout=5):
        '''
        GET请求

        :param url: 必填，发起请求的地址，例如：https://192.168.11.10:8080

        :param path: 必填，发起请求的路径，例如：/sso/login/_login

        :param cookies:可选，请求的cookies

        :param timeout: 可选，请求超时时间，单位秒，默认5秒

        :return:返回HTTP/HTTPS响应消息的文本格式

        '''
        url = url.rstrip('/') + '/' + path.lstrip('/')
        headers=self.headers
        headers['Cookie']=cookies
        response = requests.get(url, headers=headers, timeout=timeout, verify=False)
        response.close()
        return response.text

    def http_post(self, url, path, data, cookies='', timeout=5, response='yes'):
        '''
        POST请求

        :param url: 必填，发起请求的地址，例如：https://192.168.11.10:8080

        :param path: 必填，发起请求的路径，例如：/sso/login/_login

        :param data: 可选，请求消息体

        :param cookies: 可选，请求的cookies

        :param timeout: 可选，请求超时时间，单位秒，默认5秒

        :param response: 可选，是否有响应消息，默认yes

        :return: 返回HTTP/HTTPS响应消息的文本格式

        '''
        url = url.rstrip('/') + '/' + path.lstrip('/')
        data = data.encode('utf-8')
        headers=self.headers
        headers['Cookie']=cookies
        if response == 'yes':
            response = requests.post(url, headers=headers, data=data,  timeout=timeout,
                                     verify=False)
            response.close()
            return response.text
        else:
            try:
                response = requests.post(url, headers=self.headers, data=data, cookies=cookies, timeout=timeout,
                                         verify=False)
                response.close()
            except:
                pass

    def http_upload(self, url, path, files, cookies='', timeout=5, response='yes', name='file',**postdata):
        '''
        POST请求

        :param url: 必填，发起请求的地址，例如：https://192.168.11.10:8080

        :param path: 必填，发起请求的路径，例如：/sso/login/_login

        :param files: 可选，上传文件名

        :param cookies: 可选，请求的cookies

        :param timeout: 可选，请求超时时间，单位秒，默认5秒

        :param response: 可选，是否有响应消息，默认yes

        :param name: 可选，上传消息体中的name字段，默认file

        :param postdata: 可选，上传消息体中的除了name的其他字段字段，如：type=‘4’,authFileType='0'

        :return: 返回HTTP/HTTPS响应消息的文本格式

        '''

        fp = open(files, mode='rb')
        fields = {name: (files, fp.read(), 'application/octet-stream')}
        fields.update(postdata)
        fp.close()
        multipartEncoder = MultipartEncoder(fields=fields)
        self.upload_headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Content-Type': multipartEncoder.content_type
        }
        print(multipartEncoder.content_type)
        url = url.rstrip('/') + '/' + path.lstrip('/')
        headers=self.upload_headers
        headers['Cookie']=cookies
        if response == 'yes':
            response = requests.post(url, headers=headers, data=multipartEncoder,
                                     timeout=timeout, verify=False)
            response.close()
            return response.text
        else:
            try:
                response = requests.post(url, headers=headers, data=multipartEncoder,
                                         timeout=timeout,
                                         verify=False)
                response.close()
            except:
                pass

    def http_delete(self, url, path, cookies='', timeout=5, response='yes'):
        '''
        DELETE请求

        :param url: 必填，发起请求的地址，例如：https://192.168.11.10:8080

        :param path: 必填，发起请求的路径，例如：/sso/login/_login

        :param cookies: 可选，请求的cookies

        :param timeout: 可选，请求超时时间，单位秒，默认5秒

        :param response: 可选，是否有响应消息，默认yes

        :return: 返回HTTP/HTTPS响应消息的文本格式

        '''
        url = url.rstrip('/') + '/' + path.lstrip('/')
        headers=self.headers
        headers['Cookie']=cookies
        if response == 'yes':
            response = requests.delete(url, headers=headers,  timeout=timeout, verify=False)
            response.close()
            return response.text
        else:
            try:
                response = requests.delete(url, headers=headers, timeout=timeout,
                                           verify=False)
                response.close()
            except:
                pass


if __name__ == '__main__':
    a = HttpFunction()
    cookie = a.get_login_cookies('https://10.21.18.161:8686', '/maxs/pm/sso/login/_login',
                                 '{"username":"admin", "password":"H+jOOxq3q6vb6XPUgaUx4Th0jq/5s+I7QDlUEZXcgev1qH5OE0Marc4O1UzSaf3DljMQNuMv3+rZOsMnVyxpo/dPGXr5X4wQGpe+Tb9YAy0hLtx4/S8zqet84xJ74ri15DKcrbAmJofX2TnDEitXukEqoVVmK6phrIEIC2SFiUA=","captcha":"","captchaUuid":"","tenantId":-1}')
    b = a.http_upload('https://10.21.18.161:8686', '/maxs/pm/system/license/upload.do', '剧本导入测试cl.pb', cookies=cookie,
                      name='fileList')
    print(b)
    # cookies={"ssa_jwt":"eyJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2Nzc0NzU5OTQsImp0aSI6IjE2MzAwNzg1ODIyMzA5NDE2OTgiLCJ0b2tlblRpbWVvdXQiOjE4MDAsInR5cGUiOiJicm93c2VyIiwic3ViIjoiLTQiLCJwbGF0Zm9ybU1nIjowLCJ0ZW5hbnRJZCI6LTIsInVzZXJuYW1lIjoibGljZW5zZSIsIm5hbWUiOiLorrjlj6_nrqHnkIblkZgiLCJ1c2VyX3R5cGUiOjF9.Rh_nqEhi3N6Fbttb0thl4W4v13qUAkZTYNQxKaPslv20Fs1gtvcVNFzl3FATPVtDjWMnlGbr7iXBD-7SOEvKtDHQwBmv0wiK86cMZCP0_Oo6vJYCW9T5-Di4rMMBhxVFEyp1yHMKBAyubefK0HtU3wU-yo2funxh0GA68F8OM75BQkb1x980HoZf4sOKNzWC0It8D21gQWyTDkKdRNcvfILdkweOglR4K-kit7pVWscsNFYi5YrBDwacyWy4Z_z0T7PlF7aLxZkcsxOJhaVUAGt3Lk5m7WkCwSPXJ4cTvNo5Um8FO3kENCuChB8NhZk4Yo1Kv_W5wgXsd-xKhq2hqA"}
    # data='{"type":0,"topic":"MAXS_COLLECT_7","name":"tda7_test","partition":1,"replica":1,"config":{"host":52,"deviceId":3,"port":"8806"}}'
    # res=a.http_post('http://10.21.47.143','/data-access/flume/create',data,cookies)
    # print(res)
    # data={"testData":"<14>Mar 10 14:23:50 TDA-7.localdomain CEF:0|AsiaInfo-Sec|信桅高级威胁监测系统|7.0.2.2138|4|网络攻击告警事件|3|log_id='60fc4d5-64097e0b-001'    device_ip='192.168.11.219'    host_name='TDA-7.localdomain'    device_id='60fc4d56-e8fc-828e-0c3f-9e07ec67e391'    tenant_id='None'    company='AsiaInfo-Sec'    product_name='信桅高级威胁监测系统'    product_type='NGTDA'    product_version='7.0.2.2138'    Logtime=1678429430    event_time=1678429429000    flow_id='8910090419519016181'    flow_source=0    src_addr_v4='1.150.12.231'    dst_addr_v4='1.200.23.214'  src_port=65016    dst_port=80    tran_proto='tcp'    app_proto='http'    http_req_line='GET /XweMHDv HTTP/1.1'    http_req_hdr='Host: AlUGabcmbZRzJSbYvGEnJaGoXVGbqhaKU\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'    http_resp_line='HTTP/1.1 200 OK'    http_resp_hdr='Date: Tue, 22 Sep 2020 06:51:34 GMT\r\nServer: Apache/2.4.1\r\nLast-Modified: Tue, 22 Sep 2020 06:51:25 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: 292\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n'    http_resp_body='<html><body><script>var fjP\\\\=18;var kjusZDTG\\\\=9;for (var VXfnuCexLs\\\\=1;VXfnuCexLs<12;VXfnuCexLs++){for (var BFlMEp\\\\=0;BFlMEp<87;BFlMEp++){var AOspMBec\\\\=BFlMEp-2;switch(BFlMEp){case 2:case 4:case 6:case 8:case 10:case 12:}if (BFlMEp \\\\=\\\\= 70){BFlMEp\\\\= 'lWT';}}}location.reload();</script></body></html>'    url='/XweMHDv'    ret_code=200    http_method='GET'    user_agent='Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'    event_type=4    threat_class='0x4'    kill_chain_phase='0x3'  att_tac='TA0004'    att_tec='T1068'    rule_id=103021371    rule_source=0    cve=['CVE-2017-11811']    cnnvd=['CNNVD-201710-176']    affected_os='Windows'    severity=3    threat_tag=['0x53']    confidence=80    attacker_addr='1.150.12.231'    victim_addr='1.200.23.214'    attack_res=0    attack_direction=2    log_type=0"}
    # res=a.http_post('https://192.168.111.171:8686','/ssa/acm/modelInst/getColumns',data,cookie)
    # print(res)
    # b=a.http_upload('http://192.168.111.171','/maxs/pm/system/license/upload.do','161TEST-NZAOWWC99,NZMBWWC99,NZMCWWC99,N5B3WLC30,N5B5WLC30-9F5E976.dat',cookies=cookie)
    # print(b)
