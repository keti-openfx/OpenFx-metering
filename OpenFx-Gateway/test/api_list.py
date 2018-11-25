from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import random
import docker
import pymysql
import threading
import time
import subprocess



def create_memory(call_value):
  global metering_stop
  cli = docker.Client(base_url='unix://var/run/docker.sock')
  container = cli.inspect_container('my-running-server')
  container_id = container['Id']
  channel = grpc.insecure_channel(str(container['NetworkSettings']['Networks']['bridge']['IPAddress'])+':50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)

  for i in random.sample(range(30,150),call_value):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)
    time.sleep(0.12)
  print(" Over ")
  metering_stop = True

