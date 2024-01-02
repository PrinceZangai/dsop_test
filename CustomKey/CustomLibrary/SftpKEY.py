# -*-coding:utf-8 -*-
import os

import paramiko


class SftpFunction():
    def __open(self, conectinfo: dict):
        conectinfo = eval(conectinfo)
        self.host = conectinfo['host']
        self.port = int(conectinfo['port'])
        self.username = conectinfo['username']
        self.password = conectinfo['password']
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(username=self.username, password=self.password)
        self.sftp = paramiko.SFTPClient.from_transport(transport)

    def put_file_via_sftp(self, conectinfo, localfilename, remotepath):
        '''
        上传文件至服务器

        :param conectinfo: 必填，sftp连接信息，需要json格式，例如：{"host":"10.21.18.166","port":"22","username":"root","password":"11@11"}

        :param localfilename: 必填，需要上传的文件名，需放在customlibrary/logs目录下

        :param remotepath: 必填，上传至服务器上的路径及名称

        举例：Put File Via Sftp       {"host":"10.21.18.166","port":"22","username":"root","password":"1qazXSW@6yhn"}      TDA     /data/asap/TDA
        表示使用sftp连接10.21.18.166，然后吧TDA文件上传到/data/asap下，名称为TDA

        '''
        dirpath = os.path.dirname(__file__)
        logpath = os.path.join(dirpath, 'logs/{}'.format(localfilename))
        self.__open(conectinfo)
        self.sftp.put(logpath, remotepath)
        self.sftp.close()


if __name__ == '__main__':
    a = SftpFunction()
    a.put_file_via_sftp('{"host":"10.21.18.166","port":"22","username":"root","password":"1qazXSW@6yhn"}', 'TDA',
                        '/data/asap/cb/TDA')
