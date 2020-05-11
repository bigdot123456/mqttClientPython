import json
import sys
import uuid
import time

import pymysql

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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

defaultcfgName = "mqttConfig.json"
# defaultServer = "104.233.164.173"
defaultServer = "111.229.168.108"
defaultPort = 1883
defaultUsername = 'userA'
defaultPassword = 'userfast'
defaultTopic = 'mtopic'

class mqttClientMsg():
    broker = defaultServer
    port = defaultPort
    username = defaultUsername
    password = defaultPassword
    topic = defaultTopic

    clientid = 'test_mqtt_python_' + str(uuid.uuid4())

    def __init__(self, cfgName=defaultcfgName):
        self.cfgName = cfgName
        self.readconfig()
        self.initDB()

    def initDB(self):
        self.engine = create_engine(SQLCODE)
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()
        # 查询结果集, 对象模式，需要取出具体数据
        # result = s.query(AssetLoadsqldatum).all()
        # self.engine.execute(f"delete from asset_checkresultpython where ID >0; ")
        print("Open Table for write data...")
        self.engine.execute("create table IF NOT EXISTS `MACMessageTable` (`clientID` varchar(32),`time` time, `topic` varchar(32),`message` varchar(1024) ); ")

    def readconfig(self):
        try:
            print(f"start reading config files: {self.cfgName}...\n")
            with open(self.cfgName, 'r') as f:
                temp = json.loads(f.read())
                self.broker = temp.get('broker', defaultServer)
                self.port = temp.get('port', defaultPort)
                self.username = temp.get('username', defaultUsername)
                self.password = temp.get('password', defaultPassword)
                self.topic = temp.get('topic', defaultTopic)
        except :
            print(f"should check config file {self.cfgName}")

    # 连接MQTT服务器
    def on_mqtt_connect(self):
        print(f"Start communication with peer: {self.broker}...\n")
        self.mqttClient = mqtt.Client(f"{self.clientid}|securemode=3,signmethod=hmacsha1|")
        self.mqttClient.username_pw_set(self.username, self.password)
        self.mqttClient.connect(self.broker, self.port, 60)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self,topic,payload,qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self,client,userdata,msg):
        # print(msg.topic + " " + ":" + str(msg.payload))
        info=json.loads(str(msg.payload))

        self.insert_json(msg.topic,info)
        print(f"Multi msg Insert:{msg}")

    def insert_json(self,topic,info):
        for key in info:
            val = info[key]

            if len(val) > 1024:
                val=val[0:1023]
            sqlparams =f"INSERT MACMessageTable ('clientID','time','topic','message') VALUES ({key},{time.ctime()},{topic},{val}); "
            print(f"run sql:{sqlparams}")
            self.engine.execute(sqlparams)

    # subscribe 消息
    def on_subscribe(self):
        # 订阅监听自定义Topic
        self.mqttClient.subscribe("mtopic", 1)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    # @sched.scheduled_job('cron', id='my_job_id', second=1)
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

if __name__ == "__main__":
    print("Start Test Mqtt client!")
    t=mqttClientMsg()
    t.main()
