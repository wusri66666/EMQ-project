import paho.mqtt.client as mqtt
import json


def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('139.196.15.231', 1883, 600)
# client.connect('192.168.10.176', 1883, 600)

# publish task period
payload = {
    "task_id": "smartahc",
    "task_name": "smart123",
    "task_parameter": 100
}
client.publish('/app/app_qrsahyin/user/get', payload=json.dumps(payload), qos=0)

# publish other info
# payload = {
#     "username": "admin",
#     "password": "q1w2e3r4"
# }
# client.publish('/app/app_qrsahyin/user/get', payload=json.dumps(payload), qos=0)

# publish task interval
# payload = {
#     "task_id": "smartahc",
#     "task_name": "smart123",
#     "type":"interval",
#     "task_parameter": {
#         "seconds":5
#     }
#
# }

# payload = {
#     "shutdown":True
# }
# client.publish('/app/app_qrsahyin/task/push', payload=json.dumps(payload), qos=0)
