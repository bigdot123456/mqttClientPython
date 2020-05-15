#!/usr/bin/env bash
keytool -genkey -keystore MACNode.keystore -storepass FastSLL123456 -keypass activemqexample -dname "CN=ActiveMQ Artemis Server, OU=Artemis, O=ActiveMQ, L=AMQ, S=AMQ, C=AMQ" -keyalg RSA
keytool -export -keystore MACNode.keystore -file server-side-cert.cer -storepass FastSLL123456
keytool -import -keystore MACNode.truststore -file server-side-cert.cer -storepass FastSLL123456 -keypass FastSLL123456 -noprompt

# artemis config
# <acceptor name="netty-ssl-acceptor">tcp://localhost:5500?sslEnabled=true;keyStorePath=MACNode.keystore;keyStorePassword=FastSLL123456</acceptor>