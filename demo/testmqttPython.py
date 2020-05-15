# encoding: utf-8
import paho.mqtt.client as mqtt
import uuid
from datetime import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

from apscheduler.triggers.cron import CronTrigger
# Client对象构造
# MQTTHOST = "********.iot-as-mqtt.cn-shanghai.aliyuncs.com"
# MQTTPORT = 1883
# mqttClient = mqtt.Client("pythondevice2|securemode=3,signmethod=hmacsha1|")
# mqttClient.username_pw_set("pythondevice2&********", "5D1090BECB4E4AED75BD5208EA420275********")

MQTTHOST = '111.229.168.108'
MQTTPORT = 1883
clientid = 'test_mqtt_python_' + str(uuid.uuid4())
username = 'userA'
password = 'userfast'
topic = 'mtopic'

mqttClient= mqtt.Client(f"{clientid}|securemode=3,signmethod=hmacsha1|")
mqttClient.username_pw_set(username, password)


# 连接MQTT服务器
def on_mqtt_connect():
    mqttClient.connect(MQTTHOST, MQTTPORT, 60)
    mqttClient.loop_start()

# publish 消息
def on_publish(topic, payload, qos):
    mqttClient.publish(topic, payload, qos)

# 消息处理函数
def on_message_come(lient, userdata, msg):

    print(msg.topic + " " + ":" + str(msg.payload))


# subscribe 消息
def on_subscribe():
    # 订阅监听自定义Topic
    mqttClient.subscribe("mtopic", 1)
    mqttClient.on_message = on_message_come # 消息到来处理函数

# @sched.scheduled_job('cron', id='my_job_id', minute=1)
sched = BlockingScheduler()

# @sched.scheduled_job('cron', id='my_job_id', second=1)
def mainloop():
    # 自定义Topic消息上行
    on_publish("mtopic", "Hello msg!", 1)
    # 系统属性Topic消息上行
    on_publish("mtopic", "{\"method\":\"thing.service.property.set\",\"id\":\"1745506903\",\"params\":{\"Status\":1},\"version\":\"1.0.0\"}", 1)
    on_subscribe()

def main():
    on_mqtt_connect()
    sched.add_job(mainloop, 'interval', seconds=5)
    sched.start()

if __name__ == '__main__':
    main()
