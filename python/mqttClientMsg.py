import ast
import json
import signal
import ssl
import time
import uuid
from datetime import datetime
from functools import reduce

import paho.mqtt.client as mqtt
import pymysql
import sqlalchemy
from apscheduler.schedulers.blocking import BlockingScheduler

from python.mqttDB import Macmessagetable


SQLCODE="mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

global mqtt_looping
mqtt_looping = True

import sys
sys.path.append("..")
# from mqttDB import *

# https://github.com/bigdot123456/MACNode/blob/master/MACCheckMySQL.py

#SQLCODE = "mysql+pymysql://tiger:test123456!@@127.0.0.1/test?charset=utf8"
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

defaultcfgName = "../config/mqttConfig.json"
# defaultServer = "104.233.164.173"
defaultServer = "111.229.168.108"
defaultPort = 1883
defaultUsername = 'userA'
defaultPassword = 'userfast'
defaultsTopic = 'mtopic/#'
defaultpTopic = 'mtopic'
defaultsslEnable= "False"
defaultsslPath= "../ca/"

defaultSQLServer = "111.229.168.108"
defaultSQLdb="fastroot"
defaultSQLUsername = 'fastroot'
defaultSQLPassword = 'test123456'

def on_message(mq, userdata, msg):
    print("topic: %s" % msg.topic)
    print("payload: %s" % msg.payload)
    print("qos: %d" % msg.qos)

class MQTTClientWithDB():
    broker="localhost"
    port=1883
    ptopic = ""
    stopic = ""
    username = ""
    password = ""

    cfgName = "mqttConfig.json"

    def __init__(self, clientid="MQTTClient", cfgName=defaultcfgName):
        self.cfgName = cfgName
        self.clientid = clientid
        self.readconfig()
        self.initDB()

    def readconfig(self):
        try:
            print(f"start reading config files: {self.cfgName}...\n")
            with open(self.cfgName, 'r') as f:
                temp = json.loads(f.read())
                self.broker = temp.get('broker', defaultServer)
                self.port = temp.get('port', defaultPort)
                self.username = temp.get('username', defaultUsername)
                self.password = temp.get('password', defaultPassword)
                # self.SQLServer = temp.get('SQLServer ', defaultSQLServer)
                # self.SQLdb = temp.get('SQLdb ', defaultSQLdb)
                #
                # self.SQLusername = temp.get('SQLusername', defaultSQLUsername)
                # self.SQLpassword = temp.get('SQLpassword', defaultSQLPassword)
                #
                self.ptopic = temp.get('ptopic', defaultpTopic)
                self.stopic = temp.get('stopic', defaultsTopic)
                self.sslEnable=temp.get('sslEnable', defaultsslEnable)
                self.sslPath=temp.get('sslPath', defaultsslPath)
        except:
            print(f"should check config file {self.cfgName}")

    def on_connect(self,mq, userdata, rc, _):
        # subscribe when connected.
        self.mqttClient.subscribe(self.stopic)

    def on_message(mq, userdata, msg):
        print("topic: %s" % msg.topic)
        print("payload: %s" % msg.payload)
        print("qos: %d" % msg.qos)

    def mqtt_client_thread(self):
        self.mqttClient = mqtt.Client(client_id=self.clientid)
        self.mqttClient.username_pw_set(self.username, self.password)
        self.mqttClient.on_message = self.on_message  # 消息到来处理函数
        self.mqttClient.on_connect = self.on_connect
        if self.sslEnable == "True":
            cert_path = self.sslPath
            root_cert = cert_path + "ca/ca/ca.crt"
            cert_file = cert_path + "ca/client/client.crt"
            key_file = cert_path + "ca/client/client.key"
            self.mqttClient.tls_set(root_cert, certfile=cert_file, keyfile=key_file, cert_reqs=ssl.CERT_REQUIRED,
                                    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = on_message

        try:
            self.mqttClient.connect(self.broker, self.port, 15)
        except:
            print("MQTT Broker is not online. Connect later.")

        mqtt_looping = True
        print("Looping...")

        # mqtt_loop.loop_forever()
        cnt = 0
        while mqtt_looping:
            self.mqttClient.loop()
            print(f"Looping..{cnt}")
            cnt += 1
            if cnt > 20:
                try:
                    self.mqttClient.reconnect()  # to avoid 'Broken pipe' error.
                except:
                    time.sleep(1)
                cnt = 0

        print("quit mqtt thread")
        self.mqttClient.disconnect()

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
            """
CREATE TABLE if not exists `macmessagetable` (`id` int8 NOT NULL AUTO_INCREMENT,
`clientID` varchar(32),
`time` datetime, 
`topic` varchar(128),
`message` varchar(1024),
 PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
        )

    def closDB(self):
        self.s.close()

    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in sqlalchemy.inspection.inspect(obj).mapper.column_attrs}

    def list_dict_duplicate_removal(self, list_dict_data):
        run_function = lambda x, y: x if y in x else x + [y]
        return reduce(run_function, [[], ] + list_dict_data)

    def build_dict(self, seq, key):
        return dict((d[key], dict(d, index=i)) for (i, d) in enumerate(seq))

    def LoadSQLData(self):

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value AND parentID = :pValue")).params(value=100, pValue=1)

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=1000).order_by(
        #     AssetLoadsqldatum.Balance.desc())

        # self.nodeList = self.s.query(AssetLoadsqldatum).filter(text("ID < :value ")).params(value=Nums.MaxRecords).order_by(AssetLoadsqldatum.Balance.desc())
        ## for test aim, we reshuffle it! desc() means order reverse
        ## self.NodeList = self.NodeList[::2]+self.NodeList[1::2] ## error! since query object is not a list
        ## load asset_fund

        # #UserList=s.query(User)
        # UserList=s.query(User).all()
        # UserListdict = [u.__dict__ for u in UserList]
        # print(UserListdict)
        # UserListdict1 = [u._asdict() for u in UserList]
        # print(UserListdict1)

        ## 首先获得用户列表

        # phone = Column(String(32), nullable=False, comment='phone number')
        # email = Column(String(32), comment='email address')
        # password = Column(String(64), comment='md5 of password')
        # code = Column(String(10), comment='invitation code')
        # mycode = Column(String(10), comment='my invitation code')
        # id = Column(INTEGER(11), primary_key=True)
        # paypassword = Column(String(64), comment='pay password')
        #

        # 字典反转的例子 {v: k for k, v in m.items()}

        info = self.s.query(Macmessagetable.topic, Macmessagetable.clientID, Macmessagetable.message).all()
        print(info[0])

    # def initDB1(self):
    #     self.connection = pymysql.connect(host=self.SQLServer,
    #                                       user=self.SQLusername,
    #                                       password=self.SQLpassword,
    #                                       db=self.SQLdb,
    #
    #                                       charset='utf8mb4',
    #                                       cursorclass=pymysql.cursors.DictCursor)
    #
    #     with self.connection.cursor() as cursor:
    #         sql = "create table IF NOT EXISTS `MACMessageTable` (`clientID` varchar(32),`time` time, `topic` varchar(32),`message` varchar(1024) ); "
    #         cursor.execute(sql)
    #         self.connection.commit()



    def insert_hash(self, topic, msg):
        info = Macmessagetable()
        info.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # time.asctime() # time.time()
        info.message = msg
        info.clientID = topic
        self.s.add(info)

    def insert_json(self, topic, msg):
        for key in msg:
            val = msg[key]
            val=json.dumps(val)
            if len(val) > 1024:
                val = val[0:1023]
            info = Macmessagetable()
            info.time=datetime.now().strftime("%Y-%m-%d %H:%M:%S") #time.asctime() # time.time()
            info.topic=topic
            info.message=val
            info.clientID=key
            self.s.add(info)

        try:
            # result = s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).all()
            # if (result is None):
            #     s.add(node)
            # else:
            #     # 不能整体替代，只能每个值替换
            #     # s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).update(node)
            #     s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).delete()
            #     s.add(node)

            self.s.commit()
            print(f"sql insert {msg} ok!")
        except pymysql.err.IntegrityError:
            self.s.rollback()
        except sqlalchemy.orm.exc.FlushError:
            self.s.rollback()
        except Exception as result:
            print(f"sql insert: {result} error!")
            self.s.rollback()



# def main():
#     clientid = 'test_mqtt_python_' + str(uuid.uuid4())
#
#     t = MQTTClientWithDB(clientid,"mtopic")
#     t.main()

def stop_all(*args):

    mqtt_looping = False

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop_all)
    signal.signal(signal.SIGQUIT, stop_all)
    signal.signal(signal.SIGINT, stop_all)  # Ctrl-C

    print("Start Test Mqtt client 123!")
    clientid = 'test_mqtt_python_' + str(uuid.uuid4())

    t = MQTTClientWithDB(clientid)
    t.mqtt_client_thread()
    print("exit program")
    sys.exit(0)
