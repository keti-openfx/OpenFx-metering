from core.monitor import monitor

user_id='syscore'
container_id='pass'

container_monitor=monitor()
container_monitor.update(user_id,container_id)
container_monitor.request_monitoring('mem','1384c161550fb9d288cd9738b57a4f5d24880ead918483a49b83653e0f2d12fa')