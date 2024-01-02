import datetime
import logging
import random
import string
import time

TIME_FORMAT_1 = '%Y-%m-%d %H:%M:%S'

logger = logging.getLogger(__name__)


def make_url(prefix: str, suffix: str):
    """
    拼接url，一般前部为平台地址，后部为url
    """
    p = prefix.rstrip('/')
    s = suffix.lstrip('/')
    return f'{p}/{s}'


def get_now():
    """获取当前时间"""
    return datetime.datetime.now()


def get_ctime_str(fmt='%Y-%m-%d %H:%M:%S'):
    """获取当前时间字符串"""
    return datetime.datetime.now().strftime(fmt)


def get_time_days_ago(dt_obj, n, fmt='%Y-%m-%d %H:%M:%S'):
    """获取一个时间点n天前的时间"""
    days_ago = dt_obj - datetime.timedelta(days=n)
    return days_ago.strftime(fmt)


def get_time_days_later(dt_obj, n, fmt='%Y-%m-%d %H:%M:%S'):
    """获取一个时间点n天后的时间"""
    days_ago = dt_obj - datetime.timedelta(days=n)
    return days_ago.strftime(fmt)


def get_ts_ms() -> int:
    """
    获取时间戳，精确到毫秒
    :return: 时间戳
    """
    return int(time.time() * 1000)


def get_dict_keys(d: dict):
    r = list(d.keys())
    print(r)
    return r


def get_time_ranges(time_fmt=TIME_FORMAT_1):
    now = get_now()
    now_str = now.strftime(time_fmt)

    one_hour_ago = now - datetime.timedelta(hours=1)
    one_hour_ago = one_hour_ago.strftime(time_fmt)
    today = datetime.datetime(now.year, now.month, now.day)
    today_midnight = today.replace(hour=0, minute=0, second=0, microsecond=0).strftime(time_fmt)

    seven_days_ago = get_time_days_ago(now, 7, fmt=time_fmt)
    thirty_days_ago = get_time_days_ago(now, 30, fmt=time_fmt)
    ninety_days_ago = get_time_days_ago(now, 90, fmt=time_fmt)

    return {
        '最近1小时': [one_hour_ago, now_str],
        '当天': [today_midnight, now_str],
        '最近7天': [seven_days_ago, now_str],
        '最近30天': [thirty_days_ago, now_str],
        '最近90天': [ninety_days_ago, now_str],
    }


def generate_random_word(length):
    letters = string.ascii_lowercase
    word = ''.join(random.choice(letters) for _ in range(length))
    return word


def no_license_pass(ret=None):
    """
    没有license的跳过
    :param ret: 使函数返回的默认值
    :return: ret
    """

    def wrap(func):
        def inner(cls, *args, **kwargs):
            if not hasattr(cls, 'has_license'):
                return func(cls, *args, **kwargs)

            if not getattr(cls, 'has_license'):
                return ret

            return func(cls, *args, **kwargs)

        return inner

    return wrap


def pass_unittest(ret=True):
    """
    跳过执行函数
    :param ret: 使函数返回的默认值
    :return: ret
    """

    def wrap(func):
        def inner(cls, *args, **kwargs):
            return ret

        return inner

    return wrap


def retry(times: int, interval: float):
    """重试"""

    def wrap(func):
        def inner(*args, **kwargs):
            for i in range(0, times):
                try:
                    r = func(*args, **kwargs)
                except Exception as e:
                    logger.info(f'执行失败，将重试.func:{func.__name__}.params:{args},{kwargs}.err:{e}')
                    time.sleep(interval)
                    if i == times - 1:
                        raise
                else:
                    return r

        return inner

    return wrap


if __name__ == '__main__':
    ctime = get_ctime_str()
    # print(ctime)
    now = get_now()
    seven_days_ago = get_time_days_ago(now, 7)
    # print(seven_days_ago)

    print(get_time_ranges('%Y-%m-%d+%H:%M'))
    print(generate_random_word(3))
