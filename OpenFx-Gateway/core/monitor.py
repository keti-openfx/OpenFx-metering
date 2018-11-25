from log.log import metering_log

from resource import memory,cpu,disk,network


class monitor:
    def __init__(self):
        pass

    def update(self,user_id,fx_container_id):
        #db_update
        #get_id, start_time, memory_size..
        #metering_log('info','monitor start')
        pass


    def request_monitoring(self,type,container_id):
        if type=='mem':
            memory.memory_metering(container_id)
            return True
        elif type=='cpu':
            return True
        elif type=='network':
            return True
        elif type=='disk':
            return True
        elif type=='all':
            return True
        else:
            return False


    def stop_monitoring(self,type,container_id):
        if type=='mem':
            memory.memory_metering(container_id)
            return True
        elif type=='cpu':
            return True
        elif type=='network':
            return True
        elif type=='disk':
            return True
        elif type=='all':
            return True
        else:
            return False
