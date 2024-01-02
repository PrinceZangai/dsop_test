import websocket


class WsFunction():
    def __init__(self):
        pass

    def ws_getByid(self, url, path, timeout=10):
        '''
        通过直接带ID参数来访问websocket，获取返回消息
        :param url: 必填，ws请求的地址，例如：ws://10.21.18.163:80
        :param path:必填，ws请求的路径，例如：/maxs-monitor/monitorLog?2
        :param timeout:选填，默认为10s，websocket超时时间
        :return:返回websocket消息，每条消息之间用\n来分隔
        '''
        msg = ''
        i = 1
        while msg == '' and i <= 10:
            url = url.rstrip('/') + '/' + path.lstrip('/')
            ws = websocket.create_connection(url, timeout=timeout)
            try:
                while True:
                    msg = msg + ws.recv() + '\n'
            except Exception as e:
                print(e)
                pass
            ws.close()
            i += 1
        print(msg
              )
        return msg


if __name__ == '__main__':
    a = WsFunction()
    a.ws_getByid('ws://10.21.18.163', '/maxs-monitor/monitorLog?2')
