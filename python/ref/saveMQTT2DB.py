#!/usr/bin/python -u

import mysql.connector as mariadb
import paho.mqtt.client as mqtt
import ssl

mariadb_connection = mariadb.connect(user='tiger', password='test123456!@', database='test')
cursor = mariadb_connection.cursor()

# MQTT Settings
MQTT_Broker = "192.168.123.140"
MQTT_Port = 1883
Keep_Alive_Interval = 10
MQTT_Topic = "1/#"

# Subscribe
def on_connect(client, userdata, flags, rc):
  mqttc.subscribe(MQTT_Topic, 0)
  print("connected!")

def on_message(mosq, obj, msg):
  # Prepare Data, separate columns and values
  msg_clear = msg.payload.translate(None, '{}""').split(", ")
  msg_dict =    {}
  for i in range(0, len(msg_clear)):
    msg_dict[msg_clear[i].split(": ")[0]] = msg_clear[i].split(": ")[1]

  # Prepare dynamic sql-statement
  placeholders = ', '.join(['%s'] * len(msg_dict))
  columns = ', '.join(msg_dict.keys())
  sql = "INSERT INTO pws ( %s ) VALUES ( %s )" % (columns, placeholders)

  # Save Data into DB Table
  try:
      cursor.execute(sql, msg_dict.values())
      print(f"{sql}")
  except mariadb.Error as error:
      print("Error: {}".format(error))
  mariadb_connection.commit()

def on_subscribe(mosq, obj, mid, granted_qos):
  pass

mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect
# mqttc.tls_set(ca_certs="/Users/liqinghua/gopath/src/MACPower/keytool/ca/server/server.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
cert_path = "/Users/liqinghua/git/mqttClient/ca/ca/"

topic = "mtopic"
root_cert = cert_path + "ca/ca.crt"
cert_file = cert_path + "server/server.crt"
key_file = cert_path + "server/server.key"

mqttc.tls_set(root_cert,certfile = cert_file,keyfile =   key_file,cert_reqs=ssl.CERT_REQUIRED,tls_version=ssl.PROTOCOL_TLSv1_2,ciphers=None)

mqttc.username_pw_set("userA","userfast")

mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))

# Continue the network loop & close db-connection
mqttc.loop_forever()
mariadb_connection.close()