# -*-coding:utf-8 -*-
import ssl
from time import sleep

# from elasticsearch import Elasticsearch

# ##忽视证书
# context = ssl._create_unverified_context()


class EsFunction():
    def __init__(self):
        pass

#     def __connect(self, conectinfo: dict):
#         conectinfo = eval(conectinfo)
#         host = conectinfo['host']
#         port = str(conectinfo['port'])
#         protocol = conectinfo['protocol']
#         if 'http_auth' in conectinfo.keys():
#             http_auth = conectinfo['http_auth'].split(',')
#             self.es = Elasticsearch([host + ':' + port], http_auth=http_auth, scheme=protocol, ssl_context=context, )
#         else:
#             self.es = Elasticsearch([host + ':' + port], scheme=protocol, ssl_context=context, )

#     def check_count_in_es(self, conectinfo, indexname, condiction, exceptCount, timeout=0):
#         '''
#          断言方法，在es中按条件查询，效验结果条数是否正确

#         :param conectinfo: 必填，es连接信息，需要json格式，protocol必填：http，https；http_auth，选填，es认证的用户名密码
#         例如：{"protocol":"https","host":"10.21.17.202","port":"9200","http_auth":"('elastic', '1qazXSW@3edc')"}

#         :param indexname: 必填，要查询的索引名称，需要具体到日期，例如：maxs_standard_20220901

#         :param condiction:必填，查询条件，需要json格式，例如：{"filePath":"cb","FlumeIp_s":"10.21.17.202"}

#         :param exceptCount:必填，期望的查询条数

#         :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功


#         '''
#         try:
#             if not isinstance(condiction, dict):
#                 condiction = eval(condiction)
#             assert isinstance(condiction, dict)
#         except Exception as e:
#             raise RuntimeError('条件字段：{}是非json格式'.format(condiction))
#         self.__connect(conectinfo)
#         querycondiction = {"query": {"bool": {"must": []}}}
#         mustlist = []
#         for key, value in condiction.items():
#             a = {"match": {"%s" % key: "%s" % value}}
#             mustlist.append(a)
#         querycondiction['query']['bool']['must'] = mustlist
#         try:
#             timeout = int(timeout)
#             assert 600 >= timeout >= 0
#         except:
#             raise RuntimeError('超时时间只能是不超过600的正整数')
#         if timeout > 0:
#             total = ''
#             for i in range(timeout):
#                 try:
#                     query = self.es.search(index=indexname, body=querycondiction, scroll='5m', size=1)
#                     total = query['hits']['total']['value']
#                     assert int(exceptCount) == total, '效验失败，期望条数是{},实际条数是{}'.format(str(exceptCount), str(total))
#                     break
#                 except:
#                     sleep(1)
#             assert int(exceptCount) == total, '效验失败，期望条数是{},实际条数是{}'.format(str(exceptCount), str(total))
#         else:
#             query = self.es.search(index=indexname, body=querycondiction, scroll='5m', size=1)
#             total = query['hits']['total']['value']
#             assert int(exceptCount) == total, '效验失败，期望条数是{},实际条数是{}'.format(str(exceptCount), str(total))

#     def delete_index_in_es(self, conectinfo, indexname):
#         '''
#         删除索引

#         :param conectinfo: 必填，es连接信息，需要json格式，例如：{"host":"10.21.17.202","port":"9200"}

#         :param indexname: 必填，要删除的索引名称，需要具体到日期，例如：maxs_standard_20220901

#         '''
#         self.__connect(conectinfo)
#         if self.es.indices.exists(indexname):
#             return self.es.indices.delete(indexname)


# if __name__ == '__main__':
#     a = EsFunction()
#     a.check_count_in_es(
#         '{"protocol":"https","host":"192.168.11.171","port":"19200","http_auth":"elastic,maxs.PDG~2022"}',
#         'maxs_standard_20220922', '{"DEVICE_TYPE":"ASIA_TDA","equIP":"192.168.11.219"}', '4')
