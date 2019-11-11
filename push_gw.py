import subprocess,os,time,requests


def promethus_gw_push():
    job_name = 'my_custom_metrics'
    instance_name = '222.109.100.193:9000'
    f=open("/proc/metric",'r')
    data=f.read()
    f.close()
    metrics=''
    for d in data:
        metrics+=str(d)

    data=metrics.split("\n")

    for loop in range(0,len(data)-1):
        try:
            metrics=str(data[loop]).split(' ')
            payload_key='container_'+str(metrics[0])
            payload_value=metrics[1]
            response = requests.post(
                'http://222.109.100.193:9091/metrics/job/{j}/instance/{i}'.format(j=job_name, i=instance_name,), data='{k} {v}\n'.format(k=payload_key, v=payload_value))
        except Exception as e:
            print(e)
            break

while(True):
    try:
        promethus_gw_push()
    except Exception as e:
        print(e)
        time.sleep(1)
        pass
