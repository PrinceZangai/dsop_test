# -*-coding: utf-8 -*-
import datetime
import json
import re
from time import sleep

import pymysql


class MysqlFunction:
    def __init__(self):
        pass

    def __connect(self, conectinfo):
        if isinstance(conectinfo, str):
            conectinfo = json.loads(conectinfo)

        host = conectinfo['host']
        port = int(conectinfo['port'])
        user = conectinfo['user']
        passwd = conectinfo['password']
        database = conectinfo['database']
        self.db = pymysql.connect(host=host, port=port,
                                  user=user, password=passwd,
                                  database=database, charset='utf8')
        self.db_cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    def check_count_in_mysql(self, conectinfo, sql, expectCount: int, timeout=0):
        '''
        断言方法，在mysql数据执行sql，效验结果条数是否正确

        :param conectinfo:必填，mysql连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}

        :param sql:必填，需要执行的sql语句

        :param expectCount:必填，期望的结果条数

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check Count In Mysql    {"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}    SELECT * FROM UPMS_USER where `NAME` = 'test' and USERNAME='test'  10

             表示连接10.21.47.40的数据库，database为SSA，执行SELECT * FROM UPMS_USER where `NAME` = 'test' and USERNAME='test',检查返回的条数是否为10
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

    def check_returnvalue_in_mysql(self, conectinfo, sql, expectvalue: dict, timeout=0):
        '''

        断言方法，在mysql数据执行sql，效验结果条数是否正确

        :param conectinfo:必填，mysql连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}

        :param sql:必填，需要执行的sql语句

        :param expectvalue:必填，期望的结果，json格式

        :param timeout:选填，超时时间，取值：0~600，单位秒，会在指定的超时时间内一直检查数据，直到检查成功

        举例：Check Singlevalue In Mysql    {"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}    SELECT * FROM UPMS_USER where `NAME` = 'test' and USERNAME='test'    {"STATUS":"1","PHONE":"15915915911"}

             表示连接10.21.47.40的数据库，database为SSA，执行SELECT * FROM UPMS_USER where `NAME` = 'test' and USERNAME='test',检查返回的json结果中是STATUS是否等于1，PHONE等于15915915911
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
                    res = self.db_cursor.fetchmany(1)[0]
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
            res = self.db_cursor.fetchmany(1)[0]
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

    def exec_sql_in_mysql(self, conectinfo, sql):
        '''

        在mysql数据执行sql,可用于预置数据等,不返回结果

        :param conectinfo:必填，mysql连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}

        :param sql:必填，需要执行的sql语句



        '''
        self.__connect(conectinfo)
        self.db.commit()
        self.db_cursor.execute(sql)
        self.db.commit()
        self.db_cursor.close()
        self.db.close()

    def get_data_in_mysql(self, conectinfo, sql, keyname):
        '''

        在mysql数据执行sql,返回指定key的值

        :param conectinfo:必填，mysql连接信息，需要json格式，例如：{"user":"root","password":"1qazXSW@3edc","host":"10.21.47.40","port":"3306","database":"SSA"}

        :param sql:必填，需要执行的sql语句

        :param keyname:必填，需要返回的值的key


        '''
        self.__connect(conectinfo)
        self.db.commit()
        self.db_cursor.execute(sql)
        res = self.db_cursor.fetchmany(1)[0]
        print(res)
        self.db.commit()
        self.db_cursor.close()
        self.db.close()

        if keyname not in res.keys():
            raise RuntimeError('sql结果中不包含此字段：{}，查询结果为：{}'.format(keyname, str(res)))
        else:
            data = res[keyname]
            return data


if __name__ == '__main__':
    a = MysqlFunction()
    conn = '{"user":"root","password":"1qazXSW@3edc","host":"10.21.46.36","port":"3306","database":"SSA"}'
    # a.check_count_in_mysql(conn,'select * from UPMS_USER',11,'601')
    a.check_returnvalue_in_mysql(conn, 'select * from UPMS_USER', '{"ROLE":3}', 200)
    # del1="DELETE FROM UPMS_USER where name = 'chengbin' and username='chengbin';"
    # del2=" DELETE from UPMS_USER_ROLE where USER_ID in (SELECT user_id FROM UPMS_USER where name = 'chengbin' and username='chengbin')"
    # a.exec_sql_mysql(conn,del1)
    # a.exec_sql_mysql(conn, del1)
