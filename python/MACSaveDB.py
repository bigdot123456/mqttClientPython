import ast
import hashlib
import json
import os
import queue
import random
import ssl
import uuid
from datetime import datetime
from functools import reduce

import paho.mqtt.client as mqtt
import pymysql
import sqlalchemy
from apscheduler.schedulers.blocking import BlockingScheduler

from python.mqttDB import Macblockinfo

SQLCODE = "mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4"
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# https://github.com/bigdot123456/MACNode/blob/master/MACCheckMySQL.py
from mqttDB import Macmessagetable

# SQLCODE = "mysql+pymysql://tiger:test123456!@@127.0.0.1/test?charset=utf8"
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
BLOCKTIME = 10
defaultcfgName = "../config/mqttConfig.json"
# defaultServer = "104.233.164.173"
defaultServer = "111.229.168.108"
defaultPort = 1883
defaultUsername = 'userA'
defaultPassword = 'userfast'
defaultsTopic = 'mtopic/#'
defaultpTopic = 'mtopic'
defaultsslEnable = "False"
defaultsslPath = "../ca/"

defaultSQLServer = "111.229.168.108"
defaultSQLdb = "fastroot"
defaultSQLUsername = 'fastroot'
defaultSQLPassword = 'test123456'

__WinnerAward__ = 10  # 挖矿奖励
__OnlineAward__ = 5  # 参与总奖励
__OnlineNUM__=32 # 最大参与奖人数
LogPATH="./log"

class MQTTClientWithDB():
    broker = "localhost"
    port = 1883
    ptopic = ""
    stopic = ""
    username = ""
    password = ""
    q = queue.Queue()
    timestamp = ""

    cfgName = "mqttConfig.json"

    def __init__(self, clientid="MQTTClient", cfgName=defaultcfgName):
        self.current_winner = ""
        self.current_winHash = ""
        self.current_transactions = []
        self.chain = []
        self.chainIndex = 0
        self.winnerAward = 0
        self.onlineAward = 0

        # Create the genesis block
        self.new_block(previous_hash='1', proof=100)

        self.cfgName = cfgName
        self.clientid = clientid
        self.readconfig()
        self.initDB()
        self.mqttClient = mqtt.Client(f"goog|securemode=3,signmethod=hmacsha1|")
        self.mqttClient.username_pw_set(self.username, self.password)
        self.mkdir(LogPATH)
        if self.sslEnable == "True":
            cert_path = self.sslPath
            root_cert = cert_path + "ca/ca/ca.crt"
            cert_file = cert_path + "ca/client/client.crt"
            key_file = cert_path + "ca/client/client.key"
            self.mqttClient.tls_set(root_cert, certfile=cert_file, keyfile=key_file, cert_reqs=ssl.CERT_REQUIRED,
                                    tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)

    def new_block(self, proof, previous_hash):
        """
        Create a new Block in the Blockchain
        :param proof: The proof given by the Proof of Work algorithm
        :param previous_hash: Hash of previous Block
        :return: New Block
        """

        block = {
            'index': self.chainIndex,
            'timestamp': self.timestamp,
            'winner': self.current_winner,
            'winnHash': self.current_winHash,
            'transactions': self.current_transactions,
            'winnerAward': self.winnerAward,
            'onlineAward': self.onlineAward,
            'proof': proof,
            'previoushash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []

        self.chain.append(block)
        if len(self.chain) > 4:
            self.chain.pop(0)

        self.chainIndex += 1
        return block

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: Block
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def initDB(self):
        self.engine = create_engine(SQLCODE)
        # 创建会话
        session = sessionmaker(self.engine)
        self.s = session()
        self.s1 = session()
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

        self.engine.execute(
            """            
CREATE TABLE if not exists `macblockinfo` (`blocknum` int8 NOT NULL AUTO_INCREMENT,
`index` int8,
`timestamp` datetime, 
`winner` varchar(255), -- change from 256 to 255
`winnHash` varchar(64), -- bigint
`winnerAward` int,
`onlineAward` float,
`proof` int8,
`previoushash` int8,
`transactions` varchar(8192), -- should be 8192+32
 PRIMARY KEY (`blocknum`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
        )

    def closDB(self):
        self.s.close()

    def mkdir(self,path):

        folder = os.path.exists(path)

        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            print("Create log directory!")

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
                self.sslEnable = temp.get('sslEnable', defaultsslEnable)
                self.sslPath = temp.get('sslPath', defaultsslPath)
        except:
            print(f"should check config file {self.cfgName}")

    def on_mqtt_connect(self):
        self.mqttClient.connect(self.broker, self.port, 15)
        self.mqttClient.loop_start()

    # publish 消息
    def on_publish(self, topic, payload, qos):
        self.mqttClient.publish(topic, payload, qos)

    # 消息处理函数
    def on_message_come(self, client, userdata, msg):
        x = str(msg.payload, 'utf-8')
        try:
            info = ast.literal_eval(x)
            self.insert_json(msg.topic, info)
        except ValueError:
            print(f"receive error message:{x}:{info}")
        except:
            print(f"cant insert {x}:{info},try another record")

    def insert_hash(self, topic, msg):
        info = Macmessagetable()
        info.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # time.asctime() # time.time()
        info.message = msg
        info.clientID = topic
        self.s.add(info)

    def insert_json(self, topic, msg):
        for key in msg:
            val = msg[key]
            val = json.dumps(val)
            if len(val) > 1024:
                val = val[0:1023]
            info = Macmessagetable()
            info.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # time.asctime() # time.time()
            info.topic = topic
            info.message = val
            info.clientID = key
            self.s1.add(info)

            if (key == "Msg"):
                key = topic[9:-2]
                self.q.put((key, val))

        try:
            # result = s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).all()
            # if (result is None):
            #     s.add(node)
            # else:
            #     # 不能整体替代，只能每个值替换
            #     # s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).update(node)
            #     s.query(AssetLoadsqldatum).filter(AssetLoadsqldatum.ID == node.ID).delete()
            #     s.add(node)

            self.s1.commit()
            # print(f"sql insert {msg} ok!")
        except pymysql.err.IntegrityError:
            self.s1.rollback()
        except sqlalchemy.orm.exc.FlushError:
            self.s1.rollback()
        except Exception as result:
            print(f"sql insert: {result} error!")
            self.s1.rollback()

    # subscribe 消息
    def on_subscribe(self):
        # 订阅监听自定义Topic
        self.mqttClient.subscribe(self.stopic, 0)
        self.mqttClient.on_message = self.on_message_come  # 消息到来处理函数

    def mainloop(self):
        # 自定义Topic消息上行
        # self.on_publish(self.ptopic, "Hello msg!", 1)
        # 系统属性Topic消息上行
        # self.on_publish(self.ptopic,
        #                 "{\"method\":\"check it\",\"id\":\"1745506903\",\"params\":{\"Status\":1},\"version\":\"1.0.0\"}",
        #                 1)
        winner = {}
        winner["ID"] = ""
        winner["winHash"] = ""
        onlineMiner = []

        l = self.q.qsize()
        if l == 0:
            winner["ID"] = "0"
            winner["winHash"] = "Empty Block"
            self.winnerAward = 0
            self.onlineAward = 0
        else:
            self.winnerAward = __WinnerAward__
            self.onlineAward = __OnlineAward__ / min(l,__OnlineNUM__)
            self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            tsHash = hash(self.timestamp)
            hmin = 256
            for i in range(l):
                r = self.q.get()

                if (len(r[0]) > 255):
                    r_id = r[0][0:254]
                else:
                    r_id = r[0]
                # if (i < __OnlineNUM__ ):  ## limited block maxim size
                #     onlineMiner.append(r_id)
                onlineMiner.append(r_id)
                rHash = hash(r_id + r[1] + self.timestamp)
                difference = tsHash ^ rHash
                hamming = bin(difference).count("1")
                if hamming < hmin:
                    hmin = hamming

                    winner["ID"] = r_id
                    winner["winHash"] = r[1]

        self.current_winner = winner["ID"]
        # try:
        #     self.current_winHash = int(winner["winHash"][1:-2],16)
        # except:
        #     self.current_winHash =hash(winner["winHash"])
        #     self.current_winHash =hash(winner["winHash"])


        if(l>__OnlineNUM__):
            # x=randint(0,__OnlineNUM__-1)
            # m=onlineMiner[x:]+onlineMiner[:x]
            # n=m[0:__OnlineNUM__-1]
            n = random.sample(onlineMiner, __OnlineNUM__) ## 随机选取N个数据
        else:
            n=onlineMiner

        self.current_winHash = winner["winHash"][1:-2]
        self.current_transactions = n

        proof = self.proof_of_work(self.last_block)

        # Forge the new Block by adding it to the chain
        previoushash = hash(json.dumps(self.last_block))
        block = self.new_block(proof, previoushash)
        # print(f"Generate Block:\n{block}")
        print(f"Generate Block No.{self.chainIndex} at {datetime.now()}")
        with open(f"{LogPATH}/blockinfo.{datetime.now().strftime('%Y-%m-%d')}.json", 'a') as f:
            f.write(f"{block}\n")

        info = Macblockinfo()
        info.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # time.asctime() # time.time()

        info.index = self.chainIndex
        info.timestamp = self.timestamp
        info.winner = self.current_winner
        info.winnHash = self.current_winHash
        info.proof = proof
        info.previoushash = previoushash
        info.winnerAward = self.winnerAward
        info.onlineAward = self.onlineAward

        info.transactions = ' '.join(n)
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
            # print(f"sql insert {msg} ok!")
        except pymysql.err.IntegrityError:
            self.s.rollback()
        except sqlalchemy.orm.exc.FlushError:
            self.s.rollback()
        except Exception as result:
            print(f"sql insert: {result} error!")
            self.s.rollback()

    def proof_of_work(self, last_block):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof

        :param last_block: <dict> last Block
        :return: <int>
        """

        last_proof = last_block['proof']
        last_hash = self.hash(last_block)

        proof = 0
        while self.valid_proof(last_proof, proof, last_hash) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof, last_hash):
        """
        Validates the Proof
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :param last_hash: <str> The hash of the Previous Block
        :return: <bool> True if correct, False if not.
        """

        guess = f'{last_proof}{proof}{last_hash}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def main(self):
        sched = BlockingScheduler()
        self.on_mqtt_connect()
        # self.on_subscribe()
        sched.add_job(self.mainloop, 'interval', seconds=BLOCKTIME)
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
