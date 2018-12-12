from __future__ import print_function
import sys,os


import subprocess

import grpc

import random
import docker
import pymysql

import threading
import time



from flask import Flask,request
from flask_restful import Resource, Api

import os

app = Flask(__name__)

def get_memory():

    start_time = time.time()
    collector=''
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    data=cli.containers()
    for container in data:

        container_id=str((container['Id']))
        Names = str(container['Names']).replace("'","")
        Names = Names.replace("]", "")
        Names=Names[2:]
        Names=Names.replace('-','_')

        with open('/sys/fs/cgroup/memory/docker/' + str(container_id) + '/memory.usage_in_bytes', "r") as f:
            mem_size = int(f.read().replace('\n', ''))
            collector=collector+'memory_metering_'+str(container_id[:5])+'_'+str(Names)+'\t'+str(mem_size)+"\n"

        with open('/sys/fs/cgroup/cpu/docker/' + str(container_id) + '/cpuacct.usage', "r") as f:
            cpu_acct = int(f.read().replace('\n', ''))
            collector=collector+'cpu_usage_metering_'+str(container_id[:5])+'_'+str(Names)+'\t'+str(cpu_acct)+"\n"



    print("--- %s seconds ---" % (time.time() - start_time))


    return collector[:-1]
@app.route('/metrics',methods=['GET'])
def metrics():
    return get_memory()


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9089,debug=True)
