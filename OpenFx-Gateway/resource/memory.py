import pymysql
import datetime

def memory_metering(container_id):
    conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
    curs = conn.cursor()
    dt = datetime.datetime.now()

    pwd='/sys/fs/cgroup/memory/docker/'+str(container_id)+'/memory.usage_in_bytes'
    with open(pwd, "r") as f:
        mem_size = int(f.read().replace('\n', ''))
        query = "insert into memory (time, usage_size) VALUES (%s, %s)"
        data = (str(dt), (mem_size))
        curs.execute(query, data)
        conn.commit()
        conn.close()


