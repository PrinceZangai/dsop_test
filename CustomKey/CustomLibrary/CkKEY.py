# -*-coding:utf-8 -*-
import datetime
import re
from time import sleep

import clickhouse_driver


class CkFunction():
    def __init__(self):
        pass

    def __connect(self, conectinfo: dict):
        conectinfo = eval(conectinfo)
        host = conectinfo['host']
        port = int(conectinfo['port'])
        user = conectinfo['user']
        passwd = conectinfo['password']
        database = conectinfo['database']
        self.db = clickhouse_driver.connect(host=host, port=port,
                                            user=user, password=passwd,
                                            database=database)
        self.db_cursor = self.db.cursor()

    def check_count_in_ck(self, conectinfo, sql, expectCount: int, timeout=0):
        '''
        断言方法，在ck数据执行sql，效验结果条数是否正确

        :param conectinfo:必填，ck连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"9002","database":"default"}

        :param sql:必填，需要执行的sql语句

        :param expectCount:必填，期望的结果条数

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check Count ck    {"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"9002","database":"default"}    SELECT * FROM SYS_DICT  10

             表示连接10.21.47.40的数据库，database为default，执行SELECT * FROM SYS_DICT ,检查返回的条数是否为10
        '''
        try:
            timeout = int(timeout)
            assert 600 >= timeout >= 0
        except:
            raise RuntimeError('超时时间只能是不超过600的正整数')
        if timeout > 0:
            self.__connect(conectinfo)
            self.db.commit()
            row = ''
            for i in range(timeout):
                try:
                    self.db_cursor.execute(sql)
                    self.db.commit()
                    rows = self.db_cursor.rowcount
                    assert rows == int(expectCount)
                    break
                except:
                    sleep(1)
            self.db_cursor.close()
            self.db.close()
            assert rows == int(expectCount), '效验失败，期望条数是{},实际条数是{}'.format(str(expectCount), str(rows))

        else:
            self.__connect(conectinfo)
            self.db.commit()
            self.db_cursor.execute(sql)
            self.db.commit()
            rows = self.db_cursor.rowcount
            self.db_cursor.close()
            self.db.close()
            assert rows == int(expectCount), '效验失败，期望条数是{},实际条数是{}'.format(str(expectCount), str(rows))

    def check_returnvalue_in_ck(self, conectinfo, sql, expectvalue: dict, timeout=0):
        '''

        断言方法，在ck数据执行sql，效验结果条数是否正确

        :param conectinfo:必填，ck连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"9002","database":"default"}

        :param sql:必填，需要执行的sql语句

        :param expectvalue:必填，期望的结果，json格式

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check Singlevalue ck    {"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"9002","database":"default"}    select * from SYS_DICT where NAME ='高'    {"VALUE":3}

             表示连接10.21.47.40的数据库，database为default，执行select * from SYS_DICT where NAME ='高' ,检查返回的json结果中是VALUE是否等于3
        '''
        try:
            if not isinstance(expectvalue, dict):
                # 前台传布尔值会是小写的true、false需转换
                expectvalue = re.sub(':[ ]?true', ":True", expectvalue)
                expectvalue = re.sub(':[ ]?false', ":False", expectvalue)
                expectvalue = re.sub(':[ ]?null', ":None", expectvalue)
                expectvalue = eval(expectvalue)
            assert isinstance(expectvalue, dict)
        except Exception as e:
            raise RuntimeError('期望的结果：{}是非json格式'.format(expectvalue))
        try:
            timeout = int(timeout)
            assert 600 >= timeout >= 0
        except:
            raise RuntimeError('超时时间只能是不超过600的正整数')
        if timeout > 0:
            self.__connect(conectinfo)
            self.db.commit()
            res = ''
            for i in range(timeout):
                try:
                    self.db_cursor.execute(sql)
                    self.db.commit()
                    columns = self.db_cursor.columns_with_types
                    resvalue = self.db_cursor.fetchmany(1)[0]
                    columns = list((lambda x: x[0])(y) for y in columns)
                    res = dict(zip(columns, resvalue))
                    for key, value in res.items():
                        if isinstance(value, datetime.datetime):
                            value = value.strftime('%Y-%m-%d %H:%M:%S')
                        res[key] = value
                    for key, value in expectvalue.items():
                        if key not in res.keys():
                            raise RuntimeError('sql结果中不包含此字段：{}，查询结果为：{}'.format(key, str(res)))
                        else:
                            assert str(res[key]) == str(value), '效验失败，KEY:{}期望值是{},实际值是{}'.format(key, str(value),
                                                                                                  str(res[key]))
                    break
                except:
                    sleep(1)
            self.db_cursor.close()
            self.db.close()
            for key, value in res.items():
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                res[key] = value
            for key, value in expectvalue.items():
                if key not in res.keys():
                    raise RuntimeError('sql结果中不包含此字段：{}，查询结果为：{}'.format(key, str(res)))
                else:
                    assert str(res[key]) == str(value), '效验失败，KEY:{}期望值是{},实际值是{}'.format(key, str(value),
                                                                                          str(res[key]))
        else:
            self.__connect(conectinfo)
            self.db.commit()
            self.db_cursor.execute(sql)
            self.db.commit()
            columns = self.db_cursor.columns_with_types
            resvalue = self.db_cursor.fetchmany(1)[0]
            self.db_cursor.close()
            self.db.close()
            columns = list((lambda x: x[0])(y) for y in columns)
            res = dict(zip(columns, resvalue))

            for key, value in res.items():
                if isinstance(value, datetime.datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')
                res[key] = value
            for key, value in expectvalue.items():
                if key not in columns:
                    raise RuntimeError('sql结果中不包含此字段：{}，查询结果为：{}'.format(key, str(res)))
                else:
                    assert str(res[key]) == str(value), '效验失败，KEY:{}期望值是{},实际值是{}'.format(key, str(value),
                                                                                          str(res[key]))

    def exec_sql_in_ck(self, conectinfo, sql):
        '''

        在ck数据执行sql,可用于预置数据等,不返回结果

        :param conectinfo:必填，ck连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"9002","database":"default"}

        :param sql:必填，需要执行的sql语句



        '''
        self.__connect(conectinfo)
        self.db.commit()
        self.db_cursor.execute(sql)
        self.db.commit()
        self.db_cursor.close()
        self.db.close()


if __name__ == '__main__':
    a = CkFunction()
    conn = '{"user":"root","password":"1qazXSW@3edc","host":"10.21.18.166","port":"9002","database":"default"}'
    a.check_count_in_ck(conn, 'select * from default.CK_ALARM_MERGE_LOCAL limit 1', 1, 600)
    # a.exec_sql_in_ck(conn,'ALTER TABLE default.CK_ALARM_MERGE_LOCAL DELETE WHERE 1=1  ')
    # a.exec_sql_in_ck(conn,'ALTER TABLE  default.CK_SCENE_LOCAL DELETE WHERE 1=1  ')

    # a.check_returnvalue_in_ck(conn,"select * from SYS_DICT where NAME ='高'",'{"VALUE":"高"}',300)
