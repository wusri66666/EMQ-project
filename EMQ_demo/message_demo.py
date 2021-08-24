from EMQ.client.emq_client import EMQClient
from EMQ.client.emq_client_conf import EMQClientConf


def run():
    # 客户端配置
    client_cfg = EMQClientConf("139.196.15.231", 1883, "app_qrsahyin")
    # 创建设备
    iot_client = EMQClient(client_cfg)
    iot_client.connect()  # 建立连接

    def message_callback(msg):
        topic = "/app/app_qrsahyin/user/push"
        payload = msg.payload
        print(payload)
        iot_client.publish_raw_data(topic, payload)

    # 设置自定义回调
    iot_client.set_other_callback(message_callback)

    """
    订阅自定义topic, 需提前在平台配置自定义topic
    支持批量订阅（topic存放列表中），和逐个订阅（单个topic,无需放入列表）
    """
    # topic1 = "/app/smartahc/user/get"
    # topic2 = "/app/smartahc/aiot/get"
    # topic3 = "/app/smartahc/roi/get"
    # iot_client.subscribe(topic=[topic1, topic2, topic3])
    # iot_client.unsubscribe(topic1)
    #
    topic = "/app/app_qrsahyin/user/get"

    iot_client.subscribe(topic)

    iot_client.start()


if __name__ == '__main__':
    run()
