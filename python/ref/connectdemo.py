# -*-coding:utf-8-*- 
import paho.mqtt.client as mqtt


# 当连接上服务器后回调此函数
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # 放在on_connect函数里意味着
    # 重新连接时订阅主题将会被更新
    client.subscribe("topic/sub")


# 从服务器接受到消息后回调此函数
def on_message(client, userdata, msg):
    print("主题:" + msg.topic + " 消息:" + str(msg.payload))


client = mqtt.Client()
# 参数有 Client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
client.on_connect = on_connect  # 设置连接上服务器回调函数
client.on_message = on_message  # 设置接收到服务器消息回调函数
client.connect("iot.eclipse.org", 1883, 60)  # 连接服务器,端口为1883,维持心跳为60秒
client.loop_forever()
