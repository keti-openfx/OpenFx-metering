from concurrent import futures
import time

import grpc

import helloworld_pb2
import helloworld_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class Greeter(helloworld_pb2_grpc.GreeterServicer):

  def memory_usage(self,value): #1mb
     def big_dict_test():

         bd = dict()
         loop_limit = 1000*value
         for i in xrange(loop_limit):
             try:
                 k = i
                 bd[k] = '%s%s' % (k, '*' * 1024)

             except MemoryError:
                 print("[%s] error" % i)
                 return False


         for k in bd.keys():
             del bd[k]
         del bd

         return True




  def SayHello(self, request, context):
    self.memory_usage(int(request.name))
    return helloworld_pb2.HelloReply(message='Usage Memory, %s0 MB!' % request.name)


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()