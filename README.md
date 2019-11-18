# OpenFx-metering (Memory) 1.0.0-a1
## 1.  미터링용 커널 모듈 
### 1.1 Make (커널 모듈 컴파일)
```
make
```

### 1.2 Load Kernel Module (커널 모듈 적재)
```
insmod monitor.ko pid=[] container_name=[] pid_count=len(pid)
```
-----------------------

## 2.  커널 모듈 제어 
### 2.1 Excute Manager (커널 모듈 제어 스크립트 실행)
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
      - targets: ['prometheus_gw_server_ip:9091']

```
### 3.2 프로메테우스 구동
```
docker run -td -p 9090:9090 --name promethus_syscore -v prometheus.yml:/etc/prometheus/prometheus.yml prom/prometheus
```
-----------------------

### 3.3 프로메테우스 게이트웨이 구동
```
docker run -td -p 9091:9091 --name promethus_syscore_gw koreasecurity/openfx:prometheus_gw
```
-----------------------

### 3.4 Grafana 구동
```
docker run -td -p 3000:3000 --name grafana grafana/grafana
```
-----------------------

