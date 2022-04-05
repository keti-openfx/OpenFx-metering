import subprocess
import threading
import hashlib
import datetime

before_hash=''
new_hash=''
def time_print(msg):
    now = datetime.datetime.now()
    print(str(now)+"\t"+str(msg))
def active_module(pid_list):
    pid_len=(len(pid_list)-1)
    if pid_len==0:
        subprocess.check_output('rmmod monitor.ko', shell=True)
    pid_commends=''
    for loop in range(0,pid_len):
        pid_commends+=(str(pid_list[loop])+",")
    cmd="insmod monitor.ko pid="+str(pid_commends[:-1])+" pid_count="+str(pid_len)
    try:
        result = subprocess.check_output('rmmod monitor.ko',shell=True)
    except:
        time_print("Not Found Monitor Module")
    result = subprocess.check_output(cmd,shell=True)
    time_print("[info] Detection Container : " + str((len(pid_list) - 1)))
    pass

def container_manager():
    global before_hash,new_hash
    docker_info_name = "/root/monitoring/container_info"
    pid_list=[]
    while (True):
        try:
            result = subprocess.check_output( 'docker ps -q|xargs docker inspect --format \'{{.State.Pid}}, {{.ID}}\' > '+str(docker_info_name),shell=True)
            f = open(docker_info_name, 'rb')
            data=f.read()

            f.close()
            new_hash = hashlib.md5(data).hexdigest()
            if  (before_hash) != (new_hash):
                container_list = (data.decode('ascii').split("\n"))
                for id in container_list:
                    pid = id.split(",")[0]
                    pid_list.append(pid)

                active_module(pid_list)
                before_hash=new_hash
                time_print("[update] Kernel Module")
                pid_list=[]

        except Exception as e:
            time_print(e)
            pass
def init():
    time_print("[init] Monitor")
    pid_list=[]
    docker_info_name = "/root/monitoring/container_info"
    result = subprocess.check_output(
        'docker ps -q|xargs docker inspect --format \'{{.State.Pid}}, {{.ID}}\' > ' + str(docker_info_name), shell=True)
    f = open(docker_info_name, 'rb')
    data = f.read()
    container_list = (data.decode('ascii').split("\n"))
    for id in container_list:
        pid = id.split(",")[0]
        pid_list.append(pid)
    active_module(pid_list)
    time_print("[info] Detection Container : "+str((len(pid_list)-1)))
def testing_mode():
    count=int(input("How many Create Container ?:"))
    for i in range(0,count):
        subprocess.check_output("docker run -dt ubuntu",shell=True)
def remove_container():
    subprocess.check_output("docker stop $(docker ps -a -q)", shell=True)
    subprocess.check_output("docker rm $(docker ps -a -q)", shell=True)

commdas=input("ALL Remove Container ? (Y/N)")
if commdas.lower()=='y':
    remove_container()
commdas=input("Test Mode? (Y/N)")
if commdas.lower()=='y':
    testing_mode()

init()
docker_manger = threading.Thread(target=container_manager, args=())
docker_manger.start()


