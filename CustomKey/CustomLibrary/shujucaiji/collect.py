import json
import os
import time
import uuid

from requests_toolbelt import MultipartEncoder

from ..baseclass import BaseHandler


class CollectHandler(BaseHandler):
    """
    数据接入
    """

    def ftps_check(self, ftp_config):
        ftp_config = json.loads(ftp_config)
        url = self.make_url('/data-access/flume/ftp/checkConnect')
        data = {
            'proTypeChoose': 'ftps',
            'port': 21,
            'oldPassword': '',
            'hostCharset': 'UTF-8',
            'hdfsurl': '',
            'encryptionType': 1,
        }
        data.update(ftp_config)
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def ftps_check_yin(self, ftp_config):
        ftp_config = json.loads(ftp_config)
        url = self.make_url('/data-access/flume/ftp/checkConnect')
        data = {
            'proTypeChoose': 'ftps',
            'port': 990,
            'oldPassword': '',
            'hostCharset': 'UTF-8',
            'hdfsurl': '',
            'encryptionType': 2,
        }
        data.update(ftp_config)
        res = self.session.post(url, data=data).json()
        assert res['result'] == 'success', f'接口出错，url：{url}, res: {res}'

        return True

    def create_ftps(self, ftp_config):
        """
        数据接入-远程文件采集-FTPS
        隐式990，显式21
        :return:
        """
        ftp_config = json.loads(ftp_config)
        url = self.make_url(f'/data-access/flume/create')
        uid = str(uuid.uuid4())
        name = f'robot_test_{uid}'
        data = {
            "type": 2,
            "topic": f"MAXS_COLLECT_{uid}",
            "name": name,
            "partition": 1,
            "replica": 1,
            "sinkId": 2,
            "config": {
                "host": 52,
                "deviceId": 3,
                "proTypeChoose": "ftps",
                "hdfsurl": "",
                "h_iskerberos": "",
                "h_coresite": "",
                "h_hdfssite": "",
                "h_principal": "",
                "h_keytab": "",
                "h_krb": "",
                "remoteDir": "/robotTest",
                "filter": "",
                "strategy": "NATURE",
                "loadWorkNum": "1",
                "successBehavior": "RECORD",
                "collectSuffix": "",
                "algorithm": "",
                # "source.host": "192.168.111.75",
                "processor": "channel",
                "port": "21",
                # "username": "hsl",
                # "password": "123456",
                "encryptionType": "1",
                "charset": ""
            }
        }
        data['config'].update(ftp_config)
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        id_ = res['data']

        # 创建预处理
        url = self.make_url('/data-access/process/pipeline/createTask')
        data = {
            "inConfig": "",
            "outConfig": "",
            "templateId": 1,
            "name": f"robot_test_{uid}",
            "desc": f"spider for {name}",
            "spiderId": f"{id_}"
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        pipeline_id = res['data']

        # 开启预处理
        url = self.make_url('/data-access/process/pipeline/taskList')
        res = self.session.post(url, json={"pageIndex": 1, "pageSize": 100}).json()
        code = list(filter(lambda x: x['id'] == pipeline_id, res['data']['instance']))[0]['code']
        url = self.make_url(f'/data-access/process/pipeline/start/{code}')
        res = self.session.post(url).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        # 开启采集
        url = self.make_url('/data-access/flume/start')
        res = self.session.post(url, json={'id': id_}).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

        self.delete_pipeline(pipeline_id)
        self.delete_flume(id_)

        return True

    def create_https(self):
        path = os.path.dirname(__file__)
        file = os.path.join(path, 'mykeystore.jks')

        if os.path.exists(file):
            os.remove(file)

        os.chdir(path)
        os.system('expect genhttps.exp')
        time.sleep(10)

        assert os.path.exists(file), f'生成https证书出错'

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
        url = self.make_url('/data-access/flume/upload')
        res = self.session.post(url, data=multipartEncoder, headers=headers).json()
        assert res['code'] == 200, f'上传https证书失败，url：{url}, res: {res}'

        jks = res['data']['path']
        url = self.make_url('/data-access/flume/create')
        uid = str(uuid.uuid4())
        data = {
            "type": 8,
            "topic": f"MAXS_COLLECT_{uid}",
            "name": f"test_{uid}",
            "partition": 1,
            "replica": 1,
            "sinkId": 2,
            "config": {
                "host": 52,
                "deviceId": 3,
                "handleClass": "com.ailk.aus.flumeplugin.http.source.HttpServerSource",
                "agreement": "https",
                "crtPath": jks,
                "crtPwd": "123456",
                "port": "9999",
                "provider": "COMMON",
                "auth": "false",
                "auth_user": "",
                "auth_pass": "",
                "url": "/aus/test",
                "charset": "UTF-8"
            }
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'
        flume_id = res['data']
        self.start_flume(flume_id)
        time.sleep(5)

        url = self.make_url('/aus/test')
        url = url.replace('8686', '9999')

        s = """<14>Mar 10 14:23:50 TDA-7.localdomain CEF:0|AsiaInfo-Sec|信桅高级威胁监测系统|7.0.2.2138|4|网络攻击告警事件|3|log_id='60fc4d5-64097e0b-001'	device_ip='192.168.11.219'	host_name='TDA-7.localdomain'	device_id='60fc4d56-e8fc-828e-0c3f-9e07ec67e391'	tenant_id='None'	company='AsiaInfo-Sec'	product_name='信桅高级威胁监测系统'	product_type='NGTDA'	product_version='7.0.2.2138'	Logtime=1678429430	event_time=1678949415689	flow_id='2487394383755398389'	flow_source=0	src_addr_v4='111.111.111.111'	dst_addr_v4='1.200.13.234'	src_port=25096	dst_port=80	tran_proto='tcp'	app_proto='http'	http_req_line='GET /XweMHDv HTTP/1.1'	http_req_hdr='Host: Uqzea\r\nUser-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n'	http_resp_line='HTTP/1.1 200 OK'	http_resp_hdr='Date: Tue, 22 Sep 2020 06:51:33 GMT\r\nServer: Apache/2.2.3\r\nLast-Modified: Tue, 22 Sep 2020 06:51:27 GMT\r\nAccept-Ranges: bytes\r\nContent-Length: 337\r\nConnection: close\r\nContent-Type: text/html\r\n\r\n'	http_resp_body='<html><body><div id\\\\="fjP">Hhyn</div><script>window.onload\\\\=AOspMBec;function VXfnuCexLs(){{let kjusZDTG;function BFlMEp(){var QlDtTEP\\\\=5;var mAlUGabcm\\\\=new Object();kjusZDTG[12];var str\\\\=\'FvLf\';}try {body.parentNode(fSQ[13]);} catch ({ZRzJSbYv\\\\=eval(fjP.innerHTML)}){}}}function AOspMBec(){setTimeout(VXfnuCexLs,2000);}</script></body></html>'	url='/XweMHDv'	ret_code=200	http_method='GET'	user_agent='Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)'	event_type=4	threat_class='0x4'	kill_chain_phase='0x3'	att_tac='TA0004'	att_tec='T1068'	rule_id=103021123	rule_source=0	cve=['CVE-2017-11764']	cnnvd=['CNNVD-201709-505']	affected_os='多平台'	severity=3	threat_tag=['0x53']	confidence=80	attacker_addr='1.150.3.53'	victim_addr='1.200.13.234'	attack_res=0	attack_direction=2	log_type=0"""
        res = self.session.post(url, data=s).json()
        assert res['result'] == 'ok', f'接口出错，url：{url}, res: {res}'

        self.delete_flume(flume_id)
        return True

    def start_flume(self, id_):
        url = self.make_url('/data-access/flume/start')
        res = self.session.post(url, json={'id': id_}).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

    def delete_flume(self, id_):
        url = self.make_url('/data-access/flume/delete')
        data = {
            "id": id_
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

    def delete_pipeline(self,id_):
        """删除预处理"""
        url = self.make_url('/data-access/process/pipeline/deleteTask')
        data = {
            "id": id_
        }
        res = self.session.post(url, json=data).json()
        assert res['code'] == 200, f'接口出错，url：{url}, res: {res}'

