import subprocess


for i in range(0,20):
    cmd='docker run -d --name looper'+str(i)+ ' ubuntu  /bin/sh -c \'i=0; while true; do echo $i; i=$(expr $i + 1); sleep 1; done\''


    subprocess.check_output(cmd,shell=True)
