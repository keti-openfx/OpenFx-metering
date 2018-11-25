def memory_metering(container_id):
    pwd='/sys/fs/cgroup/memory/docker/'+str(container_id)+'/memory.kmem.max_usage_in_bytes'
    with open(pwd, "r") as f:
        mem_size = int(f.read().replace('\n', ''))
        print(mem_size)

