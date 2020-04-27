# mqttClientPython
百度智能云工程师已在云端配置了物接入项目“iotfreetest”，并为其创建了设备“thing01”，给主题demoTopic设置了发布和订阅权限。您可以使用MQTT客户端或调用MQTT SDK进行连接测试。连接的用户名为“iotfreetest/thing01”，密码为“YU7Tov8zFW+WuaLx9s9I3MKyclie9SGDuuNkl6o9LXo=”。也可以参考以下步骤，运行工程代码测试消息收发。

* 预安装环境  

本工程需要使用Python 3以上版本。本工程在Windows、Linux和Mac上均可运行。

* 下载项目文件  

从http://iot-demo.cdn.bcebos.com/SampleCode/TestMQTTPython.zip处下载工程文件，并解压至磁盘。

* 编译并运行  

打开命令行工具，进入目录TestMQTTPython（该目录里有一个requirements.txt文件和一个server.py文件）。然后运行"pip install -r requirements.txt && python server.py"。这时在命令行就能看到工程向百度天工发送了消息，并且自己接收了该消息。（按"Ctrl + C"可以退出运行。）

* 测试工程  

打开源代码文件，我们能看到连接IoT Hub所使用的用户名和密码。打开MQTT.fx（MQTT调试工具），使用相同的用户名和密码连接百度天工。连接完毕之后，向topic "demoTopic"发送字符串。发送的字符串会显示在“步骤3”运行测试项目的命令行中。最后，发送"exit"字符串，工程会结束运行。

* NodeJS  
试用物接入服务时，用户无需登录控制台，物接入服务的云端配置已经由百度智能云工程师预置好，可直接使用以下代码测试消息收发。有关控制台的配置方法，请参看操作指南。

## 注意事项:

工程使用SSL/TLS来连接百度天工。如果不想使用SSL/TLS，把endpoint URL换成"tcp://iotfreetest.mqtt.iot.gz.baidubce.com:1883"  
MQTT协议规定两个连接的client id不能相同。否则后连的会踢走先连的。如果两个设备都带重连的话，相同的client id会导致互踢死循环。因此工程中的client id做了随机化，避免连接间互踢的情况发生。实际使用时，请选择一种 clientID 生成规则，如影子名称、设备网卡 MAC 地址等。
本工程的用户名和密码只能访问“demoTopic”这个主题。访问其它主题会导致连接断开。  
百度智能云工程师已在云端配置了物接入项目“iotfreetest”，并为其创建了设备“thing01”，给主题demoTopic设置了发布和订阅权限。您可以使用MQTT客户端或调用MQTT SDK进行连接测试。连接的用户名为“iotfreetest/thing01”，密码为“YU7Tov8zFW+WuaLx9s9I3MKyclie9SGDuuNkl6o9LXo=”。也可以参考以下步骤，运行工程代码测试消息收发。

## 预安装环境

本工程需要使用Node.js 4以上版本。本工程在Windows、Linux和Mac上均可运行。

* 下载项目文件 

从http://iot-demo.cdn.bcebos.com/SampleCode/TestMQTTNode.zip处下载工程文件，并解压至磁盘。

* 编译并运行 

打开命令行工具，进入目录TestMQTTNode（该目录里有一个package.json文件和一个server.js文件）。然后运行"npm install && npm start"。这时在命令行就能看到工程向百度天工发送了消息，并且自己接收了该消息。（按"Ctrl + C"可以退出运行。）

* 测试工程 

打开源代码文件，我们能看到连接IoT Hub所使用的用户名和密码。打开MQTT.fx（MQTT调试工具），使用相同的用户名和密码连接百度天工。连接完毕之后，向topic "demoTopic"发送字符串。发送的字符串会显示在“步骤3”运行测试项目的命令行中。最后，发送"exit"字符串，工程会结束运行。
