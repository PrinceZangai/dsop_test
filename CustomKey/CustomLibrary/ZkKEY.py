# -*-coding:utf-8 -*-
import re
import time

from kazoo.client import KazooClient


class ZookeeperFunction():
    def __init__(self):
        pass

    def __connect(self, conectinfo):
        self.zk = KazooClient(hosts=conectinfo)
        self.zk.start()

    def stop(self):
        self.zk.stop()

    def __queryNodeData(self, path):
        if self.zk.exists(path):
            zk_result = self.zk.get(path)
            if zk_result[0] == '' or zk_result[0] is None:
                return ''
            else:
                return str(zk_result[0], encoding='utf-8')
        else:
            raise RuntimeError('The zookeeper node does not exist:%s' % path)

    def check_json_in_zk(self, conectinfo, path, expectvalue: dict, timeout=0):
        '''
        断言方法，检查zookeeper中的节点数据是否正确，需要数据为json格式

        :param conectinfo:必填，zookeeper连接信息，例如：10.21.17.202:2181

        :param path:必填，查询的节点全路径

        :param expectvalue:必填，期望的结果，需要是json格式

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check Json In Zk    10.21.17.202:2181    /ausApp/web/setting/common_setting    {"index_mode":"DAY","storage_time":"-1"}

             表示连接10.21.17.202:2181的zookeeper，检查节点/ausApp/web/setting/common_setting的值是否包含：key为index_mode，value为DAY；key为storage_time，值为-1的键值对
        '''
        self.__connect(conectinfo)
        zk_result = self.__queryNodeData(path)
        try:
            if not isinstance(zk_result, dict):
                zk_result = re.sub(':[ ]?true', ":True", zk_result)
                zk_result = re.sub(':[ ]?false', ":False", zk_result)
                zk_result = re.sub(':[ ]?null', ":None", zk_result)
                zk_result = eval(zk_result)
            assert isinstance(zk_result, dict)
        except Exception as e:
            print(e)
            raise RuntimeError('实际值：{}是非json格式'.format(zk_result))
        try:
            if not isinstance(expectvalue, dict):
                expectvalue = eval(expectvalue)
            assert isinstance(expectvalue, dict)
        except Exception as e:
            raise RuntimeError('期望值：{}是非json格式'.format(expectvalue))
        try:
            timeout = int(timeout)
            assert 600 >= timeout >= 0
        except:
            raise RuntimeError('超时时间只能是不超过600的正整数')
        if timeout > 0:
            for i in range(timeout):
                try:
                    for key, value in expectvalue.items():
                        if key in zk_result.keys():
                            assert zk_result[key] == value, (
                                '效验失败，期望KEY：{}值为{}，实际为{}'.format(key, value, zk_result[key]))
                        break
                except:
                    time.sleep(1)
            for key, value in expectvalue.items():
                if key in zk_result.keys():
                    assert zk_result[key] == value, ('效验失败，期望KEY：{}值为{}，实际为{}'.format(key, value, zk_result[key]))
                else:
                    raise RuntimeError('效验失败,在结果：{}中没有找到这个KEY:{}'.format(zk_result, key))
        else:
            for key, value in expectvalue.items():
                if key in zk_result.keys():
                    assert zk_result[key] == value, ('效验失败，期望KEY：{}值为{}，实际为{}'.format(key, value, zk_result[key]))
                else:
                    raise RuntimeError('效验失败,在结果：{}中没有找到这个KEY:{}'.format(zk_result, key))
        self.stop()

    def check_string_in_zk(self, conectinfo, path, data, timeout=0):
        '''
        断言方法，检查zookeeper中的节点数据是否正确，需要数据为string格式

        :param conectinfo:必填，zookeeper连接信息，例如：10.21.17.202:2181

        :param path:必填，查询的节点全路径

        :param expectvalue:必填，期望的结果，包含关系

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check String In Zk    10.21.17.202:2181    /ausApp/web/setting/common_setting    index_mode

             表示连接10.21.17.202:2181的zookeeper，检查节点/ausApp/web/setting/common_setting的值是否包含index_mode
        '''
        self.__connect(conectinfo)
        try:
            timeout = int(timeout)
            assert 600 >= timeout >= 0
        except:
            raise RuntimeError('超时时间只能是不超过600的正整数')
        zk_result = self.__queryNodeData(path)
        if timeout > 0:
            for i in range(timeout):
                try:
                    assert data in zk_result, ('效验失败，期望值是{},实际值是{}'.format(data, zk_result))
                    break
                except:
                    time.sleep(1)
            assert data in zk_result, ('效验失败，期望值是{},实际值是{}'.format(data, zk_result))
        else:
            assert data in zk_result, ('效验失败，期望值是{},实际值是{}'.format(data, zk_result))
        self.stop()

    def set_node_in_zk(self, conectinfo, path, data):
        '''
        在zookeeper中的设置节点数据

        :param conectinfo:必填，zookeeper连接信息，例如：10.21.17.202:2181

        :param path:必填，设置的节点全路径

        :param data:必填，设置的值

        举例：Set Node In Zk    10.21.17.202:2181    /ausApp/web/test    {"test":"1"}

             表示连接10.21.17.202:2181的zookeeper，设置节点/ausApp/web/test的值为：{"test":"1"}
        '''
        self.__connect(conectinfo)
        data = bytes(data, encoding="utf8")
        if self.zk.exists(path):
            self.zk.set(path, data)
        else:
            self.zk.create(path, data)
        self.stop()

    def delete_node_in_zk(self, conectinfo, path):
        '''
        在zookeeper中的删除节点数据

        :param conectinfo:必填，zookeeper连接信息，例如：10.21.17.202:2181

        :param path:必填，删除的节点全路径


        举例：Delete Node In Zk    10.21.17.202:2181    /ausApp/web/test

             表示连接10.21.17.202:2181的zookeeper，删除节点/ausApp/web/test
        '''
        self.__connect(conectinfo)
        if self.zk.exists(path):
            self.zk.delete(path, recursive=True)
        else:
            pass
        self.stop()

    def check_node_isExist_in_zk(self, conectinfo, path, exist='true'):
        '''
        检查zookeeper中的节点是否存在

        :param conectinfo:必填，zookeeper连接信息，例如：10.21.17.202:2181

        :param path:必填，删除的节点全路径

        :param exist:选填，值为：true，false。默认为true，表示检查节点存在，还是检查节点不存在

        举例：Check Node IsExist In Zk    10.21.17.202:2181    /ausApp/web/test    flase

             表示连接10.21.17.202:2181的zookeeper，检查节点/ausApp/web/test是否不存在
        '''
        self.__connect(conectinfo)
        if exist.lower() == 'true':
            if self.zk.exists(path):
                return True
            else:
                raise RuntimeError('效验失败,节点：{} 不存在'.format(path))
        elif exist.lower() == 'false':
            if self.zk.exists(path):
                raise RuntimeError('效验失败,节点：{} 存在'.format(path))
            else:
                return True
        self.stop()


if __name__ == '__main__':
    a = ZookeeperFunction()
    a.check_string_in_zk('10.21.17.202:2181', '/ausApp/web', '')
    a.check_json_in_zk('10.21.18.166:2181', '/ausApp/web/dataprocess/tda_dp/config.json',
                       '{"index_mode":"DAY","storage_time":"-1"}')
    a.set_node_in_zk('10.21.17.202:2181', '/ausApp/web/cb', '{"index_mode":"DAY","storage_time":"-1"}')
    a.check_node_isExist_in_zk('10.21.17.202:2181', '/ausApp/web/cb')
    a.delete_node_in_zk('10.21.17.202:2181', '/ausApp/web/cb')
    a.check_node_isExist_in_zk('10.21.17.202:2181', '/ausApp/web/cb', exist='false')
