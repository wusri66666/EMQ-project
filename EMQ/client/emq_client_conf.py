from EMQ.utils.emq_utils import str_is_empty


class EMQClientConf(object):
    def __init__(self, host, port, app_id):
        '''
        配置客户端相关信息
        host: EMQ服务地址
        port: EMQ服务端口
        '''
        self.host = host
        self.port = port
        self.app_id = app_id

        @property
        def host(self):
            if self.host == '':
                raise ValueError('You have not set the host')
            return self.host

        @host.setter
        def host(self, value):
            if str_is_empty(value):
                raise ValueError('server_ip Wrong !!!, the server_ip is empty')
            self.host = value

        @property
        def port(self):
            if self.port == '':
                raise ValueError('You have not set the port')
            return self.port

        @port.setter
        def port(self, value):
            if isinstance(value, int):
                raise ValueError('Invalid port !!!, port should be an instance of type int')
            self.port = value


        @property
        def app_id(self):
            if self.app_id == '':
                raise ValueError('You have not set the app_id')
            return self.app_id

        @app_id.setter
        def app_id(self, value):
            if str_is_empty(value):
                raise ValueError('app_id Wrong !!!, the app_id is empty')
            self.app_id = value
