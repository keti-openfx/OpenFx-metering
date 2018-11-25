import os,pymysql,datetime,docker

def create_container(image_name,memory_size):
    memory_size=1024*memory_size*1024
    os.system('docker stop my-running-server')
    cmd='docker run -itd --rm --name my-running-server  --memory '+str(memory_size)+'      -v "$PWD":/usr/src/myapp -w /usr/src/myapp       grpc/python:1.4 python3 memory_server.py'

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


print(create_container('null',32))



