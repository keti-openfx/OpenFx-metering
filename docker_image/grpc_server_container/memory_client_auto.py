from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import random
import docker

from metering import Metering
import threading
import time

container_id=''
metering_stop=False
def run():
  channel = grpc.insecure_channel(str(container['NetworkSettings']['Networks']['bridge']['IPAddress'])+':50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  for i in random.sample(range(30,150),10):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)
    time.sleep(1)
  time.sleep(1)

def thread_metering():
  metering_info = Metering()
  while(True):
    metering_info.memory_metering_run(container_id)
    time.sleep(0.1)
    if metering_stop:
      break

if __name__ == '__main__':
  cli = docker.Client(base_url='unix://var/run/docker.sock')
  container = cli.inspect_container('my-running-server')
  cli.get_image
  container_id=container['Id']
  metering_thread = threading.Thread(target=thread_metering, args=())
  metering_thread.start()
  run()
  metering_stop=True
