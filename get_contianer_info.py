import docker

cli = docker.Client(base_url='unix://var/run/docker.sock')
container = cli.inspect_container('my-running-server')
container_id = container['Id']
created_time = container['Created']
status = container['State']['Status']
ip = container['NetworkSettings']['Networks']['bridge']['IPAddress']
memory_size = container['HostConfig']['Memory']
print(memory_size)