#!/bin/bash
set -x
rm -Rf files/*
rm -Rf splits/*
rm -Rf logs/*
rm -Rf files.8885/*
rm -Rf files.8886/*
rm -Rf files.8887/*
rm -Rf tasks.8885/*
rm -Rf tasks.8886/*
rm -Rf tasks.8887/*
rm -Rf results.8885/*
rm -Rf results.8886/*
rm -Rf results.8887/*
for i in $(ps aux | grep slave | grep -v vim | grep -v grep | grep -v tail | awk '{ print $2 }'); do kill -9 $i; done
nohup ./controller.py &
nohup ./slave.py 8885 &
nohup ./slave.py 8886 &
nohup ./slave.py 8887 &
sleep 1
./client.py upload_file file.txt
./client.py upload_task task.py
./client.py run_task task.py file.txt result.txt
./client.py stop_slave 127.0.0.1:8885
./client.py stop_slave 127.0.0.1:8886
./client.py stop_slave 127.0.0.1:8887
./client.py stop_controller 127.0.0.1:8888
ls -lah files/
ls -lah files.*/
ls -lah splits/
ls -lah tasks/
ls -lah tasks.*/
ls -lah results.*/
rm nohup.out
for i in $(ps aux | grep slave | grep -v grep | grep -v vim | grep -v tail | awk '{ print $2 }'); do kill -9 $i ; done
