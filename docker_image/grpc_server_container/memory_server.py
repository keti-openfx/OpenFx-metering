from concurrent import futures
import time,datetime

import grpc,os

import helloworld_pb2
import helloworld_pb2_grpc


_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class memory(helloworld_pb2_grpc.GreeterServicer):

  def memory_usage(self,value):
      sts = datetime.datetime.now()
      bd = dict()
      loop_limit = 1000 * value
      print(self.print_heap('before loop [%s]' % loop_limit))
      for i in range(loop_limit):
          try:
              k = i
              bd[k] = '%s%s' % (k, '*' * 1024)
              if i and i % 10000 == 0:
                  print(self.print_heap('Dict %s inserted...' % i))
          except MemoryError:
              print("[%s] error" % i)
              return False
      del bd
      return True



  def print_heap(self,msg):
      # return msg
      rl = []
      if msg:
          # print msg,
          rl.append(msg)
      pid = os.getpid()
      return '1'


  def SayHello(self, request, context):
    self.memory_usage(int(request.name))
    return helloworld_pb2.HelloReply(message='Usage Memory, %s MB!' % request.name)



def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  helloworld_pb2_grpc.add_GreeterServicer_to_server(memory(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()

