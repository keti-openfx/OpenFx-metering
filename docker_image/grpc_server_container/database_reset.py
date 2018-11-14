import pymysql

conn = pymysql.connect(host='localhost', user='root', password='root', db='metering', charset='utf8')
curs = conn.cursor()
try:
    query = "truncate usage_memory"
    curs.execute(query)
    conn.commit()
    print('ok')


except Exception as e:
    print(e)
    pass

