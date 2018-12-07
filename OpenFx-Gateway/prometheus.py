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
    collector=''
    cli = docker.Client(base_url='unix://var/run/docker.sock')
    data=cli.containers()
    for container in data:

        container_id=(container['Id'])
        Names = str(container['Names'])

        Names=Names.replace("'","")

        Names = Names.replace("]", "")
        Names=Names[2:]

        with open('/sys/fs/cgroup/memory/docker/' + str(container_id) + '/memory.usage_in_bytes', "r") as f:
            mem_size = int(f.read().replace('\n', ''))
            collector=collector+'memory_metering_'+str(Names)+'\t'+str(mem_size)+"\n"
    print(collector[:-1])
    return collector[:-1]
@app.route('/metrics',methods=['GET'])
def metrics():
    return get_memory()



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9089,debug=True)
