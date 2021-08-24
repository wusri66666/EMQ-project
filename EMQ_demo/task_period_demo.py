from EMQ.client.emq_client import EMQClient
from EMQ.client.emq_client_conf import EMQClientConf
import json
from EMQ_demo.task_period import execute_task


def run():
    # 客户端配置
    client_cfg = EMQClientConf("139.196.15.231", 1883, "app_qrsahyin")
    # client_cfg = EMQClientConf("192.168.10.176", 1883, "app-t6gjzr49")
    # 创建设备
    iot_client = EMQClient(client_cfg)
    iot_client.connect()  # 建立连接

    def message_callback(msg):
        payload = json.loads(msg.payload)
        # print(str(payload,encoding="utf-8"),'======')
        task_id = payload.get('task_id')
        task_name = payload.get('task_name')
        task_parameter = payload.get('task_parameter')
        execute_task(iot_client, "app_qrsahyin", task_id, task_name, task_parameter)

    # 设置自定义回调
    iot_client.set_task_callback(message_callback)

    iot_client.start()


if __name__ == '__main__':
    run()
