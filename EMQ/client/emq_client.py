import paho.mqtt.client as mqtt
import json
import threading
from EMQ.utils.emq_utils import get_client_id, get_json, overwrite_json


class EMQClient(threading.Thread):
    def __init__(self, client_cfg):
        """
        client_cfg：客户信息，包括以下内容：
            host:  EMQ服务地址
            port: EMQ服务端口
            topic: 订阅/发布topic
        """
        super(EMQClient, self).__init__()
        self.host = client_cfg.host
        self.port = client_cfg.port
        self.app_id = client_cfg.app_id
        self.publish_result = mqtt.MQTT_ERR_SUCCESS
        self.task_id = None
        self.task_name = None
        self.task_parameter = None
        self.shadow_message_callback = None
        self.log_message_callback = None
        self.data_message_callback = None
        self.task_message_callback = None
        self.gpu_message_callback = None
        self.other_message_callback = None
        self.client = mqtt.Client(client_id=get_client_id())
        self.set_callback()

    def connect(self):
        """
        连接mqtt
        :return:
        """
        ret = self.client.connect(host=self.host, port=self.port, keepalive=60)
        # ret 0 表示连接成功，其他表示失败
        if ret != mqtt.MQTT_ERR_SUCCESS:
            return
        print("mqtt connection completed !!!")
        self.__subscribe()

    def set_callback(self):
        """
        设置回调函数
        :return:
        """
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_unsubscribe = self.on_unsubscribe
        self.client.on_log = self.on_log

    def __subscribe(self):
        """
        订阅平台下发命令topic
        :return:
        """
        # 订阅平台下发上报影子信息topic
        self.client.subscribe('/app/' + str(self.app_id) + '/shadow/push', qos=1)
        # 订阅平台下发上报运行日志topic
        self.client.subscribe('/app/' + str(self.app_id) + '/log/push', qos=1)
        # 订阅平台下发数据上传topic
        self.client.subscribe('/app/' + str(self.app_id) + '/data/upload', qos=1)
        # 订阅平台下发任务执行topic
        self.client.subscribe('/app/' + str(self.app_id) + "/task/push", qos=1)
        # 订阅平台下发获取gpu信息topic
        self.client.subscribe('/app/' + str(self.app_id) + '/gpu/push', qos=1)

    def on_connect(self, client, userdata, flags, rc):
        """
        设置连接回调
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        if rc == 0:
            print("Connection successful !!!")
        else:
            print("Connection fail !!!")

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")
            try:
                self.client.reconnect()
            except Exception as e:
                print(e)


    def on_subscribe(self, client, userdata, mid, granted_qos):
        """
        设置订阅消息回调
        :param client:
        :param userdata:
        :param mid:
        :param granted_qos:
        :return:
        """
        print("Subscribe mid = " + str(mid))

    def subscribe(self, topic):
        """
        处理订阅的topic
        :param topic:
        :return:
        """
        if isinstance(topic, str):
            self.__single_subscribe(topic)
        elif isinstance(topic, list):
            self.__batch_subscribe(topic)

    def __batch_subscribe(self, topic_list):
        """
        处理批量订阅的topic
        :param topic_list:
        :return:
        """
        for topic in topic_list:
            self.__single_subscribe(topic)

    def __single_subscribe(self, topic):
        """
        处理单个订阅的topic
        :param topic:
        :return:
        """
        self.__subscribe_result, _ = self.client.subscribe(topic, qos=1)
        if self.__subscribe_result == mqtt.MQTT_ERR_SUCCESS:
            print("You have subscribed: ", topic)
        else:
            print('Subscription failed: ', topic)

    def on_publish(self, client, userdata, mid):
        """
        设置已发布消息回调
        :param client:
        :param userdata:
        :param mid:
        :return:
        """
        if self.publish_result == mqtt.MQTT_ERR_SUCCESS:
            print("Publish success")
        else:
            print("Publish fail")

    def on_message(self, client, userdata, msg):
        """
        根据topic判断，平台操作的类型
        :param client:
        :param userdata:
        :param msg:
        :return:
        """
        if "/shadow/push" in msg.topic:
            self.on_shadow(msg)
        elif "/log/push" in msg.topic:
            self.on_smartlog(msg)
        elif "/data/upload" in msg.topic:
            self.on_data(msg)
        elif "/task/push" in msg.topic:
            self.on_task(msg)
        elif "/gpu/push" in msg.topic:
            self.on_gpu(msg)
        else:
            self.on_other(msg)

    def on_shadow(self, msg):
        """
        平台下发命令，获取影子信息
        :param msg:
        :return:
        """
        shadow_info = get_json("shadow")
        payload = msg.payload
        if self.shadow_message_callback:
            self.shadow_message_callback(payload)
        else:
            self.on_response_shadow(msg, shadow_info)

    def on_response_shadow(self, msg, shadow_info):
        """
        上报影子信息
        :param msg:
        :param data:
        :return:
        """
        topic = "/app/" + str(self.app_id) + "/shadow/get"
        payload = json.loads(msg.payload)
        if payload:
            payload = json.dumps(overwrite_json(json.dumps(payload), "shadow"))
        else:
            payload = json.dumps(shadow_info)
        self.client.publish(topic, payload, qos=1)

    def on_smartlog(self, msg):
        """
        平台下发命令，获取日志信息
        :param msg:
        :return:
        """
        log_info = {
            "info": "log"
        }
        payload = msg.payload
        if self.log_message_callback:
            self.log_message_callback(payload)
        else:
            self.on_response_smartlog(msg, log_info)

    def on_response_smartlog(self, msg, data):
        """
        上报日志信息
        :param msg:
        :param data:
        :return:
        """
        topic = "/app/" + str(self.app_id) + "/log/get"
        payload = {
            "result": data
        }
        payload = json.dumps(payload)
        self.client.publish(topic, payload, qos=1)

    def on_data(self, msg):
        """
        平台下发命令，获取数据信息
        :param msg:
        :return:
        """
        data_info = {
            "info": "data"
        }
        payload = msg.payload
        if self.data_message_callback:
            self.data_message_callback(payload)
        else:
            self.on_response_data(msg, data_info)

    def on_response_data(self, msg, data):
        """
        上报数据信息
        :param msg:
        :param data:
        :return:
        """
        topic = "/app/" + str(self.app_id) + "/data/get"
        payload = {
            "result": data
        }
        payload = json.dumps(payload)
        self.client.publish(topic, payload, qos=1)

    def on_task(self, msg):
        """
        平台下发命令，获取任务信息
        :param msg:
        :return:
        """
        task_info = {
            "info": "task"
        }
        if self.task_message_callback:
            self.task_message_callback(msg)
        else:
            self.on_response_task(msg, task_info)

    def on_response_task(self, msg, data):
        """
        上报任务信息
        :param msg:
        :param data:
        :return:
        """
        topic = "/app/" + str(self.app_id) + "/task/reply"
        payload = {
            "result": data
        }
        payload = json.dumps(payload)
        self.client.publish(topic, payload, qos=1)

    def on_gpu(self, msg):
        """
        平台下发命令，获取gpu信息
        :param msg:
        :return:
        """
        gpu_info = {
            "info": "gpu"
        }
        payload = msg.payload
        if self.gpu_message_callback:
            self.gpu_message_callback(payload)
        else:
            self.on_response_gpu(msg, gpu_info)

    def on_response_gpu(self, msg, data):
        """
        上报gpu信息
        :param msg:
        :param data:
        :return:
        """
        topic = "/app/" + str(self.app_id) + "/gpu/get"
        payload = {
            "result": data
        }
        payload = json.dumps(payload)
        self.client.publish(topic, payload, qos=1)

    def on_other(self, msg):
        """
        处理自定义信息
        :param msg:
        :return:
        """
        if self.other_message_callback:
            self.other_message_callback(msg)
        else:
            self.on_response_other(msg)

    def on_response_other(self, msg):
        """
        处理自定义信息
        :param msg:
        :param data:
        :return:
        """
        print(msg.topic)
        print(msg.payload)

    def unsubscribe(self, topic):
        """
        解除订阅
        :return:
        """
        if isinstance(topic, str):
            self.__single_unsubscribe(topic)
        elif isinstance(topic, list):
            self.__batch_unsubscribe(topic)

    def __batch_unsubscribe(self, topic_list):
        """
        批量解除订阅
        :param topic_list:
        :return:
        """
        for topic in topic_list:
            self.__single_unsubscribe(topic)

    def __single_unsubscribe(self, topic):
        """
        单个解除订阅
        :param topic:
        :return:
        """
        result, _ = self.client.unsubscribe(topic)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print("You have unsubscribed:", topic)
        else:
            print('Unsubscription failed: ', topic)

    def on_unsubscribe(self):
        """
        取消订阅回调函数
        :return:
        """
        print('取消订阅成功')

    def on_log(self, buf):
        """
        输出日志
        :param buf:
        :return:
        """
        print("Log:" + buf)

    def publish_raw_data(self, topic, payload):
        """
        发布消息
        :param topic:
        :param message:
        :return:
        """
        self.publish_result, _ = self.client.publish(topic=topic, payload=payload)

    # 用户自定义回调函数
    def set_shadow_callback(self, callback):
        self.shadow_message_callback = callback

    def set_log_callback(self, callback):
        self.log_message_callback = callback

    def set_data_callback(self, callback):
        self.data_message_callback = callback

    def set_task_callback(self, callback):
        self.task_message_callback = callback

    def set_gpu_callback(self, callback):
        self.gpu_message_callback = callback

    def set_other_callback(self, callback):
        self.other_message_callback = callback

    def run(self):
        """
        启动线程,在无限阻塞循环中调用loop（）,进入循环监听
        :return:
        """
        self.client.loop_forever()
