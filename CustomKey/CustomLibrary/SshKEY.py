# -*-coding:utf-8 -*-
import paramiko


class SshFunction():

    def __open(self, conectinfo: dict):
        conectinfo = eval(conectinfo)
        self.host = conectinfo['host']
        self.port = int(conectinfo['port'])
        self.username = conectinfo['username']
        self.password = conectinfo['password']
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(self.host, port=self.port, username=self.username, password=self.password)
        except paramiko.ssh_exception.AuthenticationException:
            self.ssh = paramiko.SSHClient()
            self.ssh.load_system_host_keys()
            self.ssh.connect(self.host, port=self.port, username=self.username, password=self.password)

    def exec_cmd_via_ssh(self, conectinfo, cmd, timeout=None):
        '''
         使用ssh登录服务器，并执行命令，返回值为命令执行结果

         :param conectinfo: 必填，ssh连接信息，需要json格式，例如：{"host":"10.21.18.166","port":"22","username":"root","password":"11@11"}

         :param cmd: 必填，执行的命令

         :param timeout: 选填，命令执行的超时时间

         举例：${res}   Exec Cmd Via Ssh       {"host":"10.21.18.166","port":"22","username":"root","password":"1qazXSW@6yhn"}     pwd
         表示使用ssh连接10.21.18.166，执行命令pwd，并返回结果给${res}

         '''
        self.__open(conectinfo)
        if timeout:
            stdin, stdout, stderr = self.ssh.exec_command(cmd, timeout=timeout)
        else:
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
        result = {}
        result_out = stdout.read()
        result_error = stderr.read()
        self.ssh.close()
        if result_error != b'':
            print(result_error)
            raise RuntimeError(result_error.decode('utf-8'))
        else:
            return result_out.decode('utf-8')


if __name__ == '__main__':
    a = SshFunction()
    res = a.exec_cmd_via_ssh('{"host":"192.168.11.171","port":"22","username":"root","password":"maxs.PDG~2022"}',
                             'sudo -u asap /usr/bin/ssh -fgN -L 19200:192.168.1.12:9200 localhost 1>&2')
    print(res)
