package testmqttjava;

import java.lang.Thread;
import java.util.UUID;
import org.eclipse.paho.client.mqttv3.IMqttMessageListener;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttMessage;

class MqttReceiver implements IMqttMessageListener {

    public void messageArrived(String topic, MqttMessage message) {
        System.out.println("MQTT message received: " + message);
        if (message.toString().equals("exit")) System.exit(0);
    }

}

public class TestMqttJavaMain {
    public static void main(String[] args) {
        final String broker       = "ssl://iotfreetest.mqtt.iot.gz.baidubce.com:1884";
        final String clientId     = "test_mqtt_java_" + UUID.randomUUID().toString();
        final String username     = "iotfreetest/thing01";
        final String password     = "YU7Tov8zFW+WuaLx9s9I3MKyclie9SGDuuNkl6o9LXo=";

        final String topic        = "demoTopic";
        final String content      = "Message from Baidu IoT demo";

        try {
            MqttConnectOptions connOpts = new MqttConnectOptions();
            connOpts.setUserName(username);
            connOpts.setPassword(password.toCharArray());

            System.out.println("Connecting to broker: " + broker);
            MqttClient mqttClient = new MqttClient(broker, clientId);
            mqttClient.connect(connOpts);
            System.out.println("Connected. Client id is " + clientId);

            mqttClient.subscribe(topic, new MqttReceiver());
            System.out.println("Subscribed to topic: " + topic);

            MqttMessage message = new MqttMessage(content.getBytes());
            mqttClient.publish(topic, message);
            System.out.println("Published message: " + content);

            Thread.sleep(Long.MAX_VALUE);
        } catch(Exception ex) {
            ex.printStackTrace();
        }
    }
}