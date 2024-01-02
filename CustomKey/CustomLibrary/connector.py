import abc
import re
import socket
import time
import typing

from .base import get_ctime_str, get_ts_ms

# 默认连接超时限制
DEFAULT_TIMEOUT = 2

# 日志发送每条间隔
LOG_SEND_INTERVAL = 0.001


class BaseConnector(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_operator(self):
        pass

    @abc.abstractmethod
    def close(self):
        pass


class SocketConnector(BaseConnector):
    """socket连接器"""

    def __init__(self, ip: str, port: int, lazy=False, context: dict = None):
        self.ip = ip
        self.port = port
        self.context = context
        if not lazy:
            self.operator = self.get_operator()
        else:
            self.operator = None

    def get_operator(self):
        skt_type = socket.SOCK_DGRAM
        skt = socket.socket(socket.AF_INET, skt_type)
        skt.settimeout(DEFAULT_TIMEOUT)
        skt.connect((self.ip, self.port))
        return skt

    def send(self, msg: str):
        """向socket发送一条日志"""
        self.check_msg(msg)
        msg = self.modify_msg(msg)
        self.operator.send(msg.encode('utf8'))
        time.sleep(LOG_SEND_INTERVAL)

    def send_log(self, log_path, close=True):
        """
        按行读取log文件发送
        :param log_path:日志文件
        :param close: 发送完成是否关闭连接
        :return:
        """
        with open(log_path, encoding='utf8') as f:
            for line in f:
                self.send(line.strip())

        if close:
            self.close()

    def send_logs(self, logs: typing.List[str]):
        for p in logs:
            self.send_log(p, close=False)

        self.close()

    def close(self):
        self.operator.close()

    def check_msg(self, msg):
        """不符合规则的消息将抛错"""
        pass

    def modify_msg(self, msg: str) -> str:
        """改变消息内容"""
        msg = self.update_msg(msg)
        return msg

    def update_msg(self, msg: str) -> str:
        current_time = get_ctime_str('%b %d %H:%M:%S')
        ts = get_ts_ms()
        msg = re.sub(r'[A-Z][a-z]{2} \d{2} \d{2}:\d{2}:\d{2}', current_time, msg, 1)
        pattern = r'event_time=(\d+)'
        event_time = f'event_time={ts}'
        msg = re.sub(pattern, event_time, msg)
        return msg

    def replace_ip(self, msg: str) -> str:
        ip_map = self.context.get('ip_map')
        if not ip_map:
            return msg

        for k, v in ip_map.items():
            msg = msg.replace(k, v)

        return msg
