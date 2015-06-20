#!/bin/bash
set -x
rm -Rf files/*
rm -Rf splits/*
rm -Rf logs/*
nohup ./controller.py &
nohup ./slave.py 8885 &
nohup ./slave.py 8886 &
nohup ./slave.py 8887 &
sleep 2
./client.py upload_file file.txt
./client.py stop_slave 127.0.0.1:8885
./client.py stop_slave 127.0.0.1:8886
./client.py stop_slave 127.0.0.1:8887
./client.py stop_controller 127.0.0.1:8888
ls -lah files/*
ls -lah splits/*
rm nohup.out
