from __future__ import print_function
import sys,os

from resource import memory,cpu,disk,network

import grpc
import test.helloworld_pb2
import test.helloworld_pb2_grpc
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
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    cli.stop(name)
    cli.remove_container(name)


def create_containers(size):
    memory_size=1024*size*1024
    cmd='docker run -itd --name my-running-server  --memory '+str(memory_size)+'      -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server.py'
    os.system(cmd)
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    container = cli.inspect_container('my-running-server')
    container_id = container['Id']
    created_time = container['Created']
    status = container['State']['Status']
    ip = container['NetworkSettings']['Networks']['bridge']['IPAddress']
    memory_sizes = container['HostConfig']['Memory']
    conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
    curs = conn.cursor()
    query = "DELETE FROM container"
    curs.execute(query)
    conn.commit()


    query = "insert into container (id, created_time, status, ip_address, memory_size) VALUES (%s, %s,%s, %s,%s)"
    data = (str(container_id), str(created_time),str(status),str(ip),str(memory_sizes))
    curs.execute(query, data)
    conn.commit()
    conn.close()
    return 0


def create_memory(call_value):
  cli = docker.Client(base_url='unix://var/run/docker.sock')
  container = cli.inspect_container('my-running-server')
  container_id = container['Id']
  channel = grpc.insecure_channel(str(container['NetworkSettings']['Networks']['bridge']['IPAddress'])+':50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)

  for i in random.sample(range(30,150),call_value):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)
    time.sleep(0.12)

  metering_stop = True

def thread_metering():
  metering_info = Metering()
  while(True):
    metering_info.memory_metering_run(container_id)
    time.sleep(0.1)
    if metering_stop:
      break


app = Flask(__name__)



@app.route('/API_call',methods=['POST'])
def API_call():
    call_value = request.form['request_value']
    call_value=int(call_value)
    metering_thread = threading.Thread(target=memory_metering, args=())
    if call_value>=1:
        metering_thread.start()
        memory_thtread = threading.Thread(target=create_memory, args=(call_value,))
        memory_thtread.start()
    return 'OK'

@app.route('/createContainer',methods=['POST'])
def createContainer():
    size = request.form['memory_size']
    print(size)
    size=int(size)
    create_containers(size)
    return 'OK'


@app.route('/deleteContainer',methods=['POST'])
def deleteContainer():
    name = request.form['container_name']
    container_name=str(name)
    db_reset()
    remove_container(container_name)
    return True


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
