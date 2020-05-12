import ast
import json
import time
import uuid

import paho.mqtt.client as mqtt
import pymysql
from apscheduler.schedulers.blocking import BlockingScheduler
# SQLCODE="mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# https://github.com/bigdot123456/MACNode/blob/master/MACCheckMySQL.py

SQLCODE = "mysql+pymysql://tiger:test123456!@@127.0.0.1/test?charset=utf8"
# const pool0 = mysql.createPool({
#   connectionLimit: 50,
#   host: '127.0.0.1',
#   user: 'tiger',
#   password: 'test123456!@',
#   database: 'test',
#   multipleStatements: true //是否允许执行多条sql语句
# });

# MQTTHOST = '111.229.168.108'
# MQTTPORT = 1883
# username = 'userA'
# password = 'userfast'

defaultcfgName = "mqttConfig.json"
# defaultServer = "104.233.164.173"
defaultServer = "111.229.168.108"
defaultPort = 1883
defaultUsername = 'userA'
defaultPassword = 'userfast'
defaultsTopic = 'mtopic/#'
defaultpTopic = 'mtopic'

defaultSQLServer = "111.229.168.108"
defaultSQLdb="fastroot"
defaultSQLUsername = 'fastroot'
defaultSQLPassword = 'test123456'

class MQTTClientWithDB():
    ptopic = ""
    stopic = ""
    username = ""
    password = ""

    cfgName = "mqttConfig.json"

    def __init__(self, clientid="MQTTClient", cfgName=defaultcfgName):
        self.cfgName = cfgName
        self.clientid = clientid
        self.readconfig()
        self.initDB1()
        self.mqttClient = mqtt.Client(f"goog|securemode=3,signmethod=hmacsha1|")
        self.mqttClient.username_pw_set(self.username, self.password)

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

    def initDB1(self):
        self.connection = pymysql.connect(host=self.SQLServer,
                                          user=self.SQLusername,
                                          password=self.SQLpassword,
                                          db=self.SQLdb,

                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

        with self.connection.cursor() as cursor:
            sql = "create table IF NOT EXISTS `MACMessageTable` (`clientID` varchar(32),`time` time, `topic` varchar(32),`message` varchar(1024) ); "
            cursor.execute(sql)
            self.connection.commit()

    def readconfig(self):
        try:
            print(f"start reading config files: {self.cfgName}...\n")
            with open(self.cfgName, 'r') as f:
                temp = json.loads(f.read())
                self.broker = temp.get('broker', defaultServer)
                self.port = temp.get('port', defaultPort)
                self.username = temp.get('username', defaultUsername)
                self.password = temp.get('password', defaultPassword)
                self.SQLServer = temp.get('SQLServer ', defaultSQLServer)
                self.SQLdb = temp.get('SQLdb ', defaultSQLdb)

                self.SQLusername = temp.get('SQLusername', defaultSQLUsername)
                self.SQLpassword = temp.get('SQLpassword', defaultSQLPassword)

                self.ptopic = temp.get('mtopic', defaultpTopic)
                self.stopic = temp.get('mtopic', defaultsTopic)
        except:
            print(f"should check config file {self.cfgName}")

    def on_mqtt_connect(self):
        self.mqttClient.connect(self.broker, self.port, 60)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self, client, userdata, msg):
        x=str(msg.payload, 'utf-8')
        try:
            # info = json.loads(x )
            info = ast.literal_eval(x)
            self.insert_json(msg.topic, info)
        except ValueError:
            print(f"receive error message:{x}")
        except:
            print(f"cant insert {x}")

    def insert_json(self, topic, info):
        for key in info:
            val = info[key]
            val=json.dumps(val)
            if len(val) > 1024:
                val = val[0:1023]
            sql = ""
            with self.connection.cursor() as cursor:
                sql = 'INSERT into MACMessageTable  (clientID,time,topic,message) VALUES ("%s", now(),"%s","%s")'
                cursor.execute(sql, (key, topic, val))
                print(f"{time.ctime()}:SQL insert {val}")
        self.connection.commit()

    # subscribe 消息
    def on_subscribe(self):
        # 订阅监听自定义Topic
        self.mqttClient.subscribe(self.stopic, 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    def mainloop(self):
        # 自定义Topic消息上行
        # self.on_publish(self.ptopic, "Hello msg!", 1)
        # 系统属性Topic消息上行
        self.on_publish(self.ptopic,
                        "{\"method\":\"check it\",\"id\":\"1745506903\",\"params\":{\"Status\":1},\"version\":\"1.0.0\"}",
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
    print("Start Test Mqtt client 123!")
    clientid = 'test_mqtt_python_' + str(uuid.uuid4())

    t = MQTTClientWithDB(clientid)
    t.main()
