from __future__ import print_function

import grpc

import helloworld_pb2
import helloworld_pb2_grpc


def run():
  channel = grpc.insecure_channel('172.17.0.6:50051')
  stub = helloworld_pb2_grpc.GreeterStub(channel)
  response = stub.SayHello(helloworld_pb2.HelloRequest(name='1'))
  print("Greeter client received: " + response.message)


if __name__ == '__main__':
  run()
