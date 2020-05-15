#!/usr/bin/env bash

sqlPY=~/git/mqttClient/python/mqttDB.py

rm -f $sqlPY
sqlacodegen --outfile $sqlPY mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4
# sqlacodegen --tables macmessagetable --outfile $sqlPY mysql+pymysql://fastroot:test123456@111.229.168.108/fastroot?charset=UTF8MB4