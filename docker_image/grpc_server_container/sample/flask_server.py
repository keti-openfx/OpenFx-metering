from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import random
import docker

from metering import Metering
import threading
import time



from flask import Flask
from flask_restful import Resource, Api

import os

container_id=''
metering_stop=False

def create_containers():
    memory_size=256
    memory_size=1024*memory_size*1024
    cmd='docker run -itd --rm --name my-running-server  --memory '+str(memory_size)+'      -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server.py'
    print(cmd)
    return os.system(cmd)


def create_memory():
  cli = docker.Client(base_url='unix://var/run/docker.sock')
  container = cli.inspect_container('my-running-server')
  container_id = container['Id']
  channel = grpc.insecure_channel(str(container['NetworkSettings']['Networks']['bridge']['IPAddress'])+':50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  for i in random.sample(range(30,150),10):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)
    time.sleep(1)
  time.sleep(1)
  metering_stop = True

def thread_metering():
  metering_info = Metering()
  while(True):
    metering_info.memory_metering_run(container_id)
    time.sleep(0.1)
    if metering_stop:
      break


app = Flask(__name__)


@app.route('/APICALL')
def APICALL():

    metering_thread = threading.Thread(target=thread_metering, args=())
    metering_thread.start()
    memory_thtread = threading.Thread(target=create_memory, args=())
    memory_thtread.start()


    return 'OK'


@app.route('/API_call')
def API_call():

    metering_thread = threading.Thread(target=thread_metering, args=())
    metering_thread.start()
    memory_thtread = threading.Thread(target=create_memory, args=())
    memory_thtread.start()


    return 'OK'
@app.route('/createContinaer')
def createContinaer():
    create_containers()
    return 'OK'



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

