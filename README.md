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
