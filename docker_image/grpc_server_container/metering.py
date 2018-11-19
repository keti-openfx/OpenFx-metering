import docker

import pymysql
import datetime
class Metering:

    def __init__(self):

        pass

    def memory_metering_run(self,container_id):
        conn = pymysql.connect(host='localhost', user='root', password='****', db='metering', charset='utf8')
        curs = conn.cursor()
        dt = datetime.datetime.now()
        print(dt)
        with open('/sys/fs/cgroup/memory/docker/' + str(container_id) + '/memory.usage_in_bytes', "r") as f:
            mem_size=int(f.read().replace('\n',''))
            query = "insert into usage_memory (time, usage_size) VALUES (%s, %s)"
            data=(str(dt),(mem_size))
            curs.execute(query,data)
            conn.commit()
            conn.close()







