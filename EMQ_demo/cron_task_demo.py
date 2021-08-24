from EMQ.client.emq_client import EMQClient
from EMQ.client.emq_client_conf import EMQClientConf
import json

from EMQ.utils.emq_utils import asynchronous_func, overwrite_json, get_json, stop_thread
from EMQ_demo.cron_task import cron_work


def run():
    # 客户端配置
    client_cfg = EMQClientConf("139.196.15.231", 1883, "app_qrsahyin")
    iot_client = EMQClient(client_cfg)
    iot_client.connect()  # 建立连接

    def message_callback(msg):
        payload = json.loads(msg.payload)
        task_id = payload.get('task_id')
        task_name = payload.get('task_name')
        task_parameter = payload.get('task_parameter')
        type = payload.get('type')
        shutdown = payload.get('shutdown')
        if not shutdown:
            obj = asynchronous_func(cron_work, iot_client, "app_qrsahyin", task_id, task_name, task_parameter, type)
            obj.start()
            data = json.dumps({"thread_id": obj.ident})
            overwrite_json(data, "thread")
        else:
            thread_id = get_json("thread").get('thread_id')
            stop_thread(thread_id)

    # 设置自定义回调
    iot_client.set_task_callback(message_callback)

    iot_client.start()


if __name__ == '__main__':
    run()
