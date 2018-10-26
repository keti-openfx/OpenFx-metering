from __future__ import print_function

import grpc

import helloworld_pb2
import helloworld_pb2_grpc
import random

def run():

  channel = grpc.insecure_channel('172.17.0.6:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)

  for i in random.sample(range(30,150),10):
    response = stub.SayHello(helloworld_pb2.HelloRequest(name=str(i)+''))
    print("Memory Pattern: " + response.message)


if __name__ == '__main__':
  run()
