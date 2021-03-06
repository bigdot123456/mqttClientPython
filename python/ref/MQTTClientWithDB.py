import json
import ssl
import time
import uuid

import paho.mqtt.client as mqtt
from apscheduler.schedulers.blocking import BlockingScheduler

# https://github.com/bigdot123456/MACNode/blob/master/MACCheckMySQL.py

# SQLCODE="mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
username = 'userA'
password = 'userfast'


class MQTTClientWithDB():
    ptopic=""
    stopic=""
    mqttClient = mqtt.Client(f"goog|securemode=3,signmethod=hmacsha1|")
    mqttClient.username_pw_set(username, password)

    def __init__(self, clientid,ptopic,stopic):
        self.clientid = clientid
        self.ptopic=ptopic
        self.stopic=stopic

    def initDB(self):
        self.engine = create_engine(SQLCODE)
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()
        # 查询结果集, 对象模式，需要取出具体数据
        # result = s.query(AssetLoadsqldatum).all()
        # self.engine.execute(f"delete from asset_checkresultpython where ID >0; ")
        print("Open Table for write data...")
        self.engine.execute(
            "create table IF NOT EXISTS `MACMessageTable` (`clientID` varchar(32),`time` time, `topic` varchar(32),`message` varchar(1024) ); ")

    def on_mqtt_connect(self):
        cert_path = "/Users/liqinghua/gopath/src/MACPower/keytool/ca/"

        root_cert = cert_path + "ca/ca.crt"
        cert_file = cert_path + "client/client.crt"
        key_file = cert_path + "client/client.key"

        self.mqttClient.tls_set(root_cert, certfile=cert_file, keyfile=key_file, cert_reqs=ssl.CERT_REQUIRED,
                      tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.mqttClient.connect(MQTTHOST, MQTTPORT, 60)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self,topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self,client, userdata, msg):
        info = json.loads(msg.payload)
        self.insert_json(msg.topic, info)


    def insert_json(self, topic, info):
        for key in info:
            val = info[key]

            if len(val) > 1024:
                val = val[0:1023]
            sqlparams = f"INSERT MACMessageTable ('clientID','time','topic','message') VALUES ({key},{time.ctime()},{topic},{val}); "
            print(f"run sql:{sqlparams}")
            self.engine.execute(sqlparams)

    # subscribe 消息
    def on_subscribe(self):
        # 订阅监听自定义Topic
        self.mqttClient.subscribe(self.stopic, 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    def mainloop(self):
        # 自定义Topic消息上行
        self.on_publish(self.ptopic, "Hello msg!", 1)
        # 系统属性Topic消息上行
        self.on_publish(self.ptopic,
                   "{\"method\":\"thing.service.property.set\",\"id\":\"1745506903\",\"params\":{\"Status\":1},\"version\":\"1.0.0\"}",
                   1)

    def main(self):
        sched = BlockingScheduler()
        self.on_mqtt_connect()
        # self.on_subscribe()
        sched.add_job(self.mainloop, 'interval', seconds=10)
        self.on_subscribe()
        sched.start()


# def main():
#     clientid = 'test_mqtt_python_' + str(uuid.uuid4())
#
#     t = MQTTClientWithDB(clientid,"mtopic")
#     t.main()

if __name__ == "__main__":
    print("Start Test Mqtt client!")
    clientid = 'test_mqtt_python_' + str(uuid.uuid4())

    t = MQTTClientWithDB(clientid, "mtopic","mtopic/#")
    t.main()
