
import os



def create_container(image_name,memory_size):
    memory_size=1024*memory_size*1024
    cmd='docker run -itd --rm --name my-running-server  --memory '+str(memory_size)+'      -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server2.py'
    print(cmd)
    return os.system(cmd)


print(create_container('null',20))


