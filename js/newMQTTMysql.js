//https://gist.github.com/smching/ff414e868e80a6ee2fbc8261f8aebb8f#file-app_mqtt_mysql_completed-js
var mqtt = require('mqtt'); //https://www.npmjs.com/package/mqtt
var Topic = '#'; //subscribe to all topics
var Broker_URL = 'mqtt://111.229.168.108';
var Database_URL = '111.229.168.108';

var options = {
    clientId: 'MyMQTT',
    port: 1883,
    username: 'userA',
    password: 'userfast',
    keepalive: 60
};

var client = mqtt.connect(Broker_URL, options);
client.on('connect', mqtt_connect);
client.on('reconnect', mqtt_reconnect);
client.on('error', mqtt_error);
client.on('message', mqtt_messsageReceived);
client.on('close', mqtt_close);

function mqtt_connect() {
    //console.log("Connecting MQTT");
    client.subscribe(Topic, mqtt_subscribe);
};

function mqtt_subscribe(err, granted) {
    console.log("Subscribed to " + Topic);
    if (err) {
        console.log(err);
    }
};

function mqtt_reconnect(err) {
    //console.log("Reconnect MQTT");
    //if (err) {console.log(err);}
    client = mqtt.connect(Broker_URL, options);
};

function mqtt_error(err) {
    //console.log("Error!");
    //if (err) {console.log(err);}
};

function after_publish() {
    //do nothing
};

//receive a message from MQTT broker
function mqtt_messsageReceived(topic, message, packet) {
    var message_str = message.toString(); //convert byte array to string

    message_str = message_str.replace(/\n$/, ''); //remove new line
    //payload syntax: clientID,topic,message
    // var s = JSON.stringify(message) //add type buffer key-value, we can't accept it.

    var a = JSON.parse(message_str)
    insert_json(topic, a)

    if (countInstances(message_str) != 1) {
        console.log("Multi msg Insert:" + message_str);

        // console.log("Invalid payload");
    } else {
        // insert_message(topic, message_str, packet);

     }
}
// SQL
// create  table MACMessageTable (
// clientID  VARCHAR(25),
// topic VARCHAR(63),
// message VARCHAR(1023)
// )

function insert_json(topic, jsonObj) {

    let sql = "INSERT INTO ?? (??,??,??) VALUES (?,?,?)";
    let sqlexec=""

    for (let key in jsonObj) {
        let val = jsonObj[key]
        console.log(key + ":" + val)
        if (val.length>1024)val=val.slice(0,1023)
        var params = ['MACMessageTable', 'clientID', 'topic', 'message', key, topic, val];
        sqlexec = mysql.format(sql, params);
        console.log("Message added: " + sqlexec);
        connection.query(sqlexec, function (error, results) {
            if (error) throw error;
            // console.log("Message added: " + sqlexec);
        });
    }
}

function mqtt_close() {
    console.log("Close MQTT");
}

////////////////////////////////////////////////////
///////////////////// MYSQL ////////////////////////
////////////////////////////////////////////////////
var mysql = require('mysql'); //https://www.npmjs.com/package/mysql
//Create Connection
var connection = mysql.createConnection({
    host: Database_URL,
    user: "fastroot",
    password: "test123456",
    database: "fastroot"
});

connection.connect(function (err) {
    if (err) throw err;
    console.log("Database Connected!");
});

//insert a row into the tbl_messages table
function insert_message(topic, message_str, packet) {
    var message_arr = extract_string(message_str); //split a string into an array
    var clientID = message_arr[0];
    var message = message_arr[1];
    var sql = "INSERT INTO ?? (??,??,??) VALUES (?,?,?)";
    var params = ['tbl_messages', 'clientID', 'topic', 'message', clientID, topic, message];
    sql = mysql.format(sql, params);

    connection.query(sql, function (error, results) {
        if (error) throw error;
        console.log("Message added: " + message_str);
    });
};

//split a string into an array of substrings
function extract_string(message_str) {
    var message_arr = message_str.split(","); //convert to array
    return message_arr;
};

//count number of delimiters in a string
var delimiter = ",";

function countInstances(message_str) {
    var substrings = message_str.split(delimiter);
    return substrings.length - 1;
};