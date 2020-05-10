var Mqtt = require('mqtt');
var RandomString = require('randomstring');

// var mqttParam = {
//     server: 'ssl://iotfreetest.mqtt.iot.gz.baidubce.com:1884',
//     options: {
//         username: 'iotfreetest/thing01',
//         password: 'YU7Tov8zFW+WuaLx9s9I3MKyclie9SGDuuNkl6o9LXo=',
//         clientId: 'test_mqtt_node_' + RandomString.generate()
//     },
//     topic: 'demoTopic'
// };
var mqttParam = {
     server: 'mqtt://111.229.168.108:1883',
     options: {
         username: 'userA',
         password: 'userfast',
         clientId: 'test_mqtt_node_' + RandomString.generate()
     },
     topic: 'mtopic/js'
};

var mqttClient = Mqtt.connect(mqttParam.server, mqttParam.options);
console.log('Connecting to broker: ' + mqttParam.server);

mqttClient.on('error', function(error) {
    console.error(error);
});

mqttClient.on('message', function(topic, data) {
    console.log('MQTT message received: ' + data);
    if (data.toString() === 'exit') process.exit();
});

mqttClient.on('connect', function() {
    console.log('Connected. Client id is: ' + mqttParam.options.clientId);

    mqttClient.subscribe(mqttParam.topic);
    console.log('Subscribed to topic: ' + mqttParam.topic)

    mqttClient.publish(mqttParam.topic, 'Message from MAC:');
    console.log('MQTT message published.');
});
