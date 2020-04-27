import json
import sys
import uuid

import paho.mqtt.client as mqtt

defaultcfgName = "mqttServer.json"
defaultServer = "104.233.164.173"
defaultServer = "111.229.168.108"
defaultPort = 1883
defaultUsername = 'userA'
defaultPassword = 'userfast'
defaultTopic = 'mTopic'

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

    def readconfig(self):
        try:
            with open(self.cfgName, 'r') as f:
                temp = json.loads(f.read())
                self.broker = temp.get('broker', defaultServer)
                self.port = temp.get('port', defaultPort)
                self.username = temp.get('username', defaultUsername)
                self.password = temp.get('password', defaultPassword)
                self.topic = temp.get('topic', defaultTopic)
        except :
            print(f"should check config file {self.cfgName}")

    def on_connect(self, userdata, rc):
        print('Connected. Client id is: ' + self.clientid)
        self.client.subscribe(self.topic)
        print('Subscribed to topic: ' + self.topic)

        self.client.publish(self.topic, f'Message from {defaultServer}:')
        print('MQTT message published.')

    def on_message(self, userdata, msg):
        msg = str(msg.payload, 'utf-8')
        print('MQTT message received: ' + msg)
        if msg == 'exit':
            sys.exit()

    def loop_forever(self):
        self.client = mqtt.Client(self.clientid)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.username_pw_set(self.username, self.password)

        print('Connecting to broker: ' + self.broker)
        self.client.connect(self.broker, self.port)

        self.client.loop_forever()


if __name__ == "__main__":
    print("Start Test Mqtt client!")
    t = mqttClientMsg()
    t.loop_forever()
