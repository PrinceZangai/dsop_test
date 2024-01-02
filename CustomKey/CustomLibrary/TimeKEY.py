# -*-coding: utf-8 -*-
import datetime


class TimeFunction():
    def get_Date(self, unit, value, format):
        '''
        获取指定时间的指定格式的str返回

        :param unit: 必填，单位，可填值：weeks,days,hours,minutes,seconds,microseconds,milliseconds

        :param value:必填，整形，时间增减值，表示用当前时间增加或者减少的时间，可填值：1,-1等

        :param format:必填，返回的时间格式，例如：'%Y-%m-%d %H:%M:%S','%Y-%m-%d %H:%M:%S.%f','%Y%m%d%H%M%S'

        :return:返回指定时间的字符串格式，例如：2022-08-17 17:01:01.530

        举例：Get Date    days    0    %Y-%m-%d %H:%M:%S.%f
            表示取当前时间，返回指定的带毫秒的string字段
            Get Date String    days    +1    %Y-%m-%d 00:00:00
            表示取明天的0点0分0秒
        '''
        a = eval('datetime.timedelta({})'.format(unit + '=' + str(value)))
        time = (datetime.datetime.now() + a).strftime(format)
        if '%f' in format:
            time = time[:-3]
        return time


if __name__ == '__main__':
    a = TimeFunction()
    print(a.get_Date('days', '-1', '%Y-%m-%d %H:%M:%S.%f'))
