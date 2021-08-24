import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + msg.payload.decode('utf-8'))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('139.196.15.231', 1883, 600) # 600为keepalive的时间间隔
# client.connect('192.168.10.176', 1883, 600) # 600为keepalive的时间间隔

# subscribe task period
# client.subscribe('/app/app_qrsahyin/smartahc/task/period', qos=0)
# client.subscribe('/app/app-t6gjzr49/task_123/task/period', qos=0)
# client.subscribe('/app/app_qrsahyin/smartahc/task/period', qos=0)

# subscribe other info
client.subscribe('/app/app_qrsahyin/user/push', qos=0)

client.loop_forever() # 保持连接