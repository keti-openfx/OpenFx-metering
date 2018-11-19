
import os

import sys



def create_container(image_name,memory_size):
    os.system('docker stop my-running-server')
    #cmd='docker run -itd --rm --name my-running-server  --memory '+str(memory_size)+'m      -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server2.py'
    cmd = 'docker run -itd --rm --name my-running-server  -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server.py'
    print(cmd)
    return os.system(cmd)

#mem_size=sys.argv[1].replace("\n",'')

create_container('null',256)


