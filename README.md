# OpenFx-metering (Memory) 1.0.0-a1
## 1.  미터링용 커널 모듈 컴파일 하기
### 1.1 Make
```
make
```

### 1.2 Load Kernel Module
```
insmod monitor.ko pid=[] container_name=[] pid_count=len(pid)
```
-----------------------

## 2.  커널 모듈 제어 
### 2.1 Excute Manager
```
python3.* kernel_manager.py 
```
-----------------------


## 3.  프로메테우스 게이트웨이 구동 (Using Docker)
### 3.1 prometheus.yml 설정
```
global:
  scrape_interval: 1s

scrape_configs:
  - job_name: 'pushgateway'
    honor_labels: true
    static_configs:
      - targets: ['prometheus_server_ip:9091']

```
-----------------------
