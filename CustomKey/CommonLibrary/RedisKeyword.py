import redis


class RedisKeyword:
    def __init__(self,host=None,port=None,db=None,password=None) -> None:
        self.conn = redis.Redis(host=host, port=port, db=db, password=password)

    def get_connection(self,host=None,port=None,db=None,password=None):
        if host==None:
            return self.conn
        return redis.Redis(host=host,port=port,db=db,password=password)

    def execute_command(self,command,*arg,**options):
        return self.conn.execute_command(command,*arg,**options)

if __name__=="__main__":
    r=RedisKeyword("10.21.16.39",16379,2,'!QAZxsw2#EDC(0Ol1)')
    value=r.conn.hget('ssa_login_info_1713798935533400066','upms_user_token_')
    print()
