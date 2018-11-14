import docker


class Metering:
    def __init__(self):
        self
        pass

    def memory_metering_run(self,container_id):
        f = open('/sys/fs/cgroup/memory/docker/' + str(container_id) + '/memory.usage_in_bytes')
        print(f.read())






