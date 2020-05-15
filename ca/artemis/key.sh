#!/usr/bin/env bash
keytool -genkey -keystore activemq.example.keystore -storepass activemqexample -keypass activemqexample -dname "CN=ActiveMQ Artemis Server, OU=Artemis, O=ActiveMQ, L=AMQ, S=AMQ, C=AMQ" -keyalg RSA
keytool -export -keystore activemq.example.keystore -file server-side-cert.cer -storepass activemqexample
keytool -import -keystore activemq.example.truststore -file server-side-cert.cer -storepass activemqexample -keypass activemqexample -noprompt
