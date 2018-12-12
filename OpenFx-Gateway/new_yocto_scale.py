from __future__ import print_function
import sys,os

from core.monitor import monitor
import subprocess

import grpc
import test.helloworld_pb2 as helloworld_pb2
import test.helloworld_pb2_grpc as helloworld_pb2_grpc
import random
import docker
import pymysql

import threading
import time



from flask import Flask,request
from flask_restful import Resource, Api

import os
import requests
container_id=''
metering_stop=False

port_global=5000


def db_reset():
    conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
    curs = conn.cursor()
    try:
        query = "truncate memory"
        curs.execute(query)
        query = "truncate container"
        curs.execute(query)
        conn.commit()
        return True
    except Exception as e:
        print(e)
        pass

def remove_container(name):
    try:
        cli = docker.Client(base_url='unix://var/run/docker.sock')
        cli.stop(name)
        cli.remove_container(name)
    except:
        pass


def create_containers(size,container_name,port):
    memory_size=1024*size*1024
    data=''
    f=open('/root/memory_usage/mem.py','r')
    while(True):
        get_data=f.readline()
        if get_data=='':
            break
        data+=get_data
    f.close()
    data=data.replace('new_port',str(port))
    f = open('/root/memory_usage/mem_new.py', 'w')
    for i in data:
        f.write(str(i))
    f.close()

    cmd='docker run -d -v /root/memory_usage/mem_new.py:/root/server.py --name '+str(container_name)+' -p '+str(port)+':'+str(port)+'  --memory '+str(memory_size)+' memory_ubuntu /usr/bin/python3 /root/server.py'
    try:
        result=subprocess.check_output(cmd,shell=True)
        if str(result).find('Error')>=0:
            return False

        cli = docker.Client(base_url='unix://var/run/docker.sock')
        names=container_name
        container = cli.inspect_container(container_name)
        container_id = container['Id']
        created_time = container['Created']
        status = container['State']['Status']
        print(status)
        ip = container['NetworkSettings']['Networks']['bridge']['IPAddress']
        memory_sizes = container['HostConfig']['Memory']
        conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
        curs = conn.cursor()
        #query = "DELETE FROM container"
        #curs.execute(query)
        #conn.commit()

        query = "insert into container (id, created_time, status, ip_address, memory_size, container_name) VALUES (%s, %s,%s, %s,%s,%s)"
        data = (str(container_id), str(created_time),str(status),str(ip),str(memory_sizes),str(names))
        curs.execute(query, data)
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        return False
    return True


def create_memory(call_value,port):
  global metering_stop
  for i in random.sample(range(5, 30), call_value):
      with requests.Session() as new_session:
          link = 'http://127.0.0.1:'+str(port)
          params = {'memory': str(i)}
          data = new_session.get(link, params=params)
          print(data)
          print(data.text)
  metering_stop = True

def thread_metering(container_id):
  global metering_stop
  metering_info = monitor()
  print(container_id)
  while(True):
    metering_info.request_monitoring("mem",container_id)
    time.sleep(0.1)
    if metering_stop:
      break


app = Flask(__name__)



@app.route('/API_call',methods=['POST'])
def API_call():
    global metering_stop
    metering_stop=False
    print(request.form)
    call_value = request.form['request_value']
    container_id= request.form['container_id']
    call_value=int(call_value)

    cli = docker.Client(base_url='unix://var/run/docker.sock')
    container = cli.inspect_container(container_id)
    port=container['NetworkSettings']['Ports']
    port=list(port.keys())
    port=port[0].replace('/tcp','')
    print(port)

    metering_thread = threading.Thread(target=thread_metering, args=(container_id,))
    if call_value>=1:
        metering_thread.start()
        memory_thtread = threading.Thread(target=create_memory, args=(call_value,port,))
        memory_thtread.start()
    return 'OK'



@app.route('/createContainer',methods=['POST'])
def createContainer():
    #db_reset()
    global port_global
    port_global+=1

    size = request.form['memory_size']
    container_name = request.form['new_container_name']
    size=int(size)
    result=create_containers(size,str(container_name),port_global)
    #remove_container(container_name)
    if request:
        return 'OK'
    else:
        return 'ERROR'



@app.route('/deleteContainer',methods=['POST'])
def deleteContainer():
    #db_reset()
    name = request.form['container_name']
    container_name=str(name)
    print(container_name)
    #db_reset()
    conn = pymysql.connect(host='localhost', user='root', password='syscore))%@', db='metering', charset='utf8')
    curs = conn.cursor()
    query = 'delete from container where container_name = \''+str(name)+'\';'
    print(query)
    curs.execute(query)
    conn.commit()

    remove_container(container_name)
    return 'OK'


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
