import uuid

import paho.mqtt.client as mqtt
from apscheduler.schedulers.blocking import BlockingScheduler

# https://github.com/bigdot123456/MACNode/blob/master/MACCheckMySQL.py

# SQLCODE="mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4"
SQLCODE = "mysql+pymysql://tiger:test123456!@@127.0.0.1/test?charset=utf8"
# const pool0 = mysql.createPool({
#   connectionLimit: 50,
#   host: '127.0.0.1',
#   user: 'tiger',
#   password: 'test123456!@',
#   database: 'test',
#   multipleStatements: true //是否允许执行多条sql语句
# });

MQTTHOST = '111.229.168.108'
MQTTPORT = 1883
clientid = 'test_mqtt_python_' + str(uuid.uuid4())
username = 'userA'
password = 'userfast'
topic = 'mtopic'

mqttClient= mqtt.Client(f"{clientid}|securemode=3,signmethod=hmacsha1|")
mqttClient.username_pw_set(username, password)

class MQTTClientWithDB():

    def on_mqtt_connect(self):
        mqttClient.connect(MQTTHOST, MQTTPORT, 60)
        mqttClient.loop_start()

    # publish 消息
    def on_publish(self,topic, payload, qos):
        mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self,client, userdata, msg):
        print(msg.topic + " " + ":" + str(msg.payload))

    # subscribe 消息
    def on_subscribe(self):
        # 订阅监听自定义Topic
        mqttClient.subscribe("mtopic", 1)
        mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    def mainloop(self):
        # 自定义Topic消息上行
        self.on_publish("mtopic", "Hello msg!", 1)
        # 系统属性Topic消息上行
        self.on_publish("mtopic",
                   "{\"method\":\"thing.service.property.set\",\"id\":\"1745506903\",\"params\":{\"Status\":1},\"version\":\"1.0.0\"}",
                   1)
        self.on_subscribe()

    def main(self):
        sched = BlockingScheduler()
        self.on_mqtt_connect()
        sched.add_job(self.mainloop, 'interval', seconds=5)
        sched.start()


def main():
    t = MQTTClientWithDB()
    t.main()



if __name__ == "__main__":
    print("Start Test Mqtt client!")
    main()
