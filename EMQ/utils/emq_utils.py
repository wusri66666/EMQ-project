import threading
import time
import os
import json
import datetime
import ctypes
import inspect


def str_is_empty(value):
    '''
    判断参数 value是否为空（空包括：None; ''; 全部为空格）
    :param value:字符串或者None
    '''
    if value == None:
        return True
    if not isinstance(value, str):
        raise ValueError('Input parameter value is not string')
    return value.strip() == ''


def get_client_id():
    """
    获取客户ID
    client_id是连接到代理。如果client_id的长度为零或为零，则行为为由使用的协议版本定义。如果使用MQTT v3.1.1，
    那么一个零长度的客户机id将被发送到代理，代理将被发送为客户端生成一个随机变量。如果使用MQTT v3.1，那么id将是
    随机生成的。在这两种情况下，clean_session都必须为True。如果这在这种情况下不会产生ValueError。
    注意：一般情况下如果客户端服务端启用两个监听那么客户端client_id 不能与服务器相同，如这里用时间"20190222142358"作为它的id，
    如果与服务器id相同，则无法接收到消息
    """
    client_id = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    return client_id


def get_json(name):
    """
    获取配置文件
    """
    BASE_DIR = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    file_address = os.path.join(BASE_DIR, 'conf/%s.json' % name)
    with open(file_address) as f:
        conf = json.loads(f.read())
    return conf


def overwrite_json(data, name):
    """
    重写配置文件
    """
    BASE_DIR = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    file_address = os.path.join(BASE_DIR, 'conf/%s.json' % name)
    with open(file_address, 'w') as f:
        f.write(data)


def get_time_now():
    """
    获取当前时间
    :return: 当前时间
    """
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time_now


def asynchronous(outter):
    """
    多线程装饰器
    :param outter:
    :return:
    """

    def wrapper(*args, **kwargs):
        threading.Thread(target=outter, args=args, kwargs=kwargs).start()

    return wrapper


def asynchronous_func(func, *args, **kwargs):
    obj = threading.Thread(target=func, args=args, kwargs=kwargs)
    return obj


# 停止线程
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(threadId):
    _async_raise(threadId, SystemExit)
