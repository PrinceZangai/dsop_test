# -*-coding:utf-8 -*-
import datetime
import os
import random
import re
import time
from socket import *
from time import sleep

year = datetime.datetime.now().year
day = datetime.datetime.now().day
if len(str(day)) == 1: day = '0' + str(day)
month = datetime.datetime.now().month
if len(str(month)) == 1: month = '0' + str(month)
month_en = ''
if str(month) == '01':
    month_en = "Jan"
elif str(month) == '02':
    month_en = "Feb"
elif str(month) == '03':
    month_en = "Mar"
elif str(month) == '04':
    month_en = "Apr"
elif str(month) == '05':
    month_en = "May"
elif str(month) == '06':
    month_en = "Jun"
elif str(month) == '07':
    month_en = "Jul"
elif str(month) == '08':
    month_en = "Aug"
elif str(month) == '09':
    month_en = "Sep"
elif str(month) == '10':
    month_en = "Oct"
elif str(month) == '11':
    month_en = "Nov"
elif str(month) == '12':
    month_en = "Dec"
match1 = '[0-9]{4}-[0-9]{1,2}-[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
match2 = '[a-zA-z]{3}\s+[0-9]{1,2} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
match3 = '[a-zA-z]{3}\s+[0-9]{1,2} [0-9]{4} [0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
match4 = '[0-9]{2}\/[a-zA-z]{3}\/[0-9]{4}:[0-9]{1,2}:[0-9]{1,2}:[0-9]{1,2}'
match5 = 'event_time=\d*'


class SendUdpFunction():
    def send_udp(self, host, port: int, logname, sendnum):
        '''
        发送UDP消息函数，目前支持的数据类型为：tda

        :param host:必填，发送消息的对端ip

        :param port:必填，发送消息的对端端口

        :param logname:必填，要发送的日志，目前支持：tda

        :param sendnum:必填，发送数据的总数

        举例：Send Udp   192.168.1.1   8803    tda 10000
            表示向192.168.1.1:8803发送10000条tda日志
        '''
        dirpath = os.path.dirname(__file__)
        logpath = os.path.join(dirpath, 'logs/{}'.format(logname))
        if not os.path.exists(logpath):
            raise RuntimeError('目前不支持{}设备的日志发送'.format(logname))
        try:
            port = int(port)
            sendnum = int(sendnum)
            assert port > 0
            assert sendnum > 0
        except:
            raise RuntimeError('端口和发送数量都必须为正整数')
        mSocket = socket(AF_INET, SOCK_DGRAM)
        nowtime = (datetime.datetime.now() - datetime.timedelta(minutes=1)).strftime('%H:%M:')
        i = 0
        for j in range(100000000):
            with open(logpath, encoding='UTF-8') as f:
                for line in f:
                    t = time.time()
                    t1 = str(round(t * 1000))
                    line = re.sub(match1, '{}-{}-{} {}'.format(year, month, day, nowtime + str(random.randint(10, 59))),
                                  line)
                    line = re.sub(match2, '{} {} {}'.format(month_en, day, nowtime + str(random.randint(10, 59))), line)
                    line = re.sub(match3,
                                  '{} {} {} {}'.format(month_en, day, year, nowtime + str(random.randint(10, 59))),
                                  line)
                    line = re.sub(match4,
                                  '{}/{}/{}:{}'.format(day, month_en, year, nowtime + str(random.randint(10, 59))),
                                  line)
                    line = re.sub(match5, 'event_time={}'.format(t1), line)
                    mSocket.sendto(line.encode("utf-8"), (host, port))
                    i += 1
                    if i >= sendnum: return sendnum
                    if i % 10 == 0:
                        sleep(0.005)


if __name__ == '__main__':
    a = SendUdpFunction()
    a.send_udp('10.10.10.1', 15666, 'tda', 100)
