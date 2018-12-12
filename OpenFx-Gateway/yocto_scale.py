from __future__ import print_function
import sys,os

from core.monitor import monitor
import subprocess

import grpc
import test.helloworld_pb2 as helloworld_pb2
import test.helloworld_pb2_grpc as helloworld_pb2_grpc
import random
import docker
import pymysql

import threading
import time



from flask import Flask,request
from flask_restful import Resource, Api

import os

container_id=''
metering_stop=False



def db_reset():
    conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
    curs = conn.cursor()
    try:
        query = "truncate memory"
        curs.execute(query)
        query = "truncate container"
        curs.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        pass

def remove_container(name):
    try:
        cli = docker.Client(base_url='unix://var/run/docker.sock')
        cli.stop(name)
        cli.remove_container(name)
    except:
        pass


def create_containers(size,container_name):
    memory_size=1024*size*1024
    cmd='docker run -itd --name '+str(container_name)+'  --memory '+str(memory_size)+'      -v "$PWD/test/conatiner":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server.py'
    try:
        result=subprocess.check_output(cmd,shell=True)
        if str(result).find('Error')>=0:
            return False

        cli = docker.Client(base_url='unix://var/run/docker.sock')
        names=container_name
        container = cli.inspect_container(container_name)
        container_id = container['Id']
        created_time = container['Created']
        status = container['State']['Status']
        print(status)
        ip = container['NetworkSettings']['Networks']['bridge']['IPAddress']
        memory_sizes = container['HostConfig']['Memory']
        conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
        curs = conn.cursor()
        query = "DELETE FROM container"
        curs.execute(query)
        conn.commit()


        query = "insert into container (id, created_time, status, ip_address, memory_size, container_name) VALUES (%s, %s,%s, %s,%s,%s)"
        data = (str(container_id), str(created_time),str(status),str(ip),str(memory_sizes),str(names))
        curs.execute(query, data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def create_memory(call_value):
  global metering_stop
  cli = docker.Client(base_url='unix://var/run/docker.sock')
  container = cli.inspect_container('gRPC-Server')
  container_id = container['Id']
  channel = grpc.insecure_channel(str(container['NetworkSettings']['Networks']['bridge']['IPAddress'])+':50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)

  for i in random.sample(range(15,150),call_value):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)


  metering_stop = True

def thread_metering():
  global metering_stop
  metering_info = monitor()

  while(True):
    metering_info.request_monitoring("mem",container_id)
    time.sleep(0.1)
    if metering_stop:
      break


app = Flask(__name__)



@app.route('/API_call',methods=['POST'])
def API_call():
    global metering_stop
    metering_stop=False
    call_value = request.form['request_value']
    call_value=int(call_value)
    metering_thread = threading.Thread(target=thread_metering, args=())
    if call_value>=1:
        metering_thread.start()
        memory_thtread = threading.Thread(target=create_memory, args=(call_value,))
        memory_thtread.start()
    return 'OK'



@app.route('/createContainer',methods=['POST'])
def createContainer():
    #db_reset()


    size = request.form['memory_size']
    container_name = request.form['new_container_name']
    size=int(size)
    result=create_containers(size,str(container_name))
    remove_container(container_name)
    if request:
        return 'OK'
    else:
        return 'ERROR'



@app.route('/deleteContainer',methods=['POST'])
def deleteContainer():
    db_reset()
    name = request.form['container_name']
    container_name=str(name)
    db_reset()
    remove_container(container_name)
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
