## 环境要求

- 已成功安装并配置Kubernetes集群

## 实验一：pod 健康管理

- 创建一个包含liveness probe的pod（master节点）

```bash
vim kubia-liveness-probe.yaml 
# 为了解探针检测失败后Kubernetes的处理方案，此处使用的是一个包含错误的镜像
apiVersion: v1
kind: Pod
metadata:
  name: kubia-liveness
spec:
  containers:
  - image: luksa/kubia-unhealthy
    name: kubia
    livenessProbe:
      httpGet:
        path: /
        port: 8080
# 创建pod
kubectl create -f kubia-liveness-probe.yaml
```

- 查看liveness probe

```bash
# 查看pod状态
kubectl get po kubia-liveness
# 查看pod详情，包括重启次数、重启原因等
kubectl describe po kubia-liveness
```



## 实验二：使用RC、RS、DS 实现容器多个副本的自动部署并持续监控副本数量

### RC

- 创建RC并查看当前pod

```bash
vim kubia-rc.yaml
# 期待pod数量为3
apiVersion: v1
kind: ReplicationController
metadata:
  name: kubia
spec:
  replicas: 3
  selector:
    app: kubia
  template:
    metadata:
      labels:
        app: kubia
    spec:
      containers:
      - name: kubia
        image: luksa/kubia
        ports:
        - containerPort: 8080
# 创建RC
kubectl create -f kubia-rc.yaml
# 查看RC信息
kubectl get rc
# 查看pod会发现Kubernetes创建了三个新的pod并随机部署在node上面
kubectl get pods
```

- 删除pod或更改pod标签，RC会自动创建或删除相应数量的pod以维持pod数量是期待值

```bash
# 删除pod
kubectl delete pod kubia-4l45m  
# 更改pod标签
kubectl label pod kubia-4l45m app=kubia
```

- 删除RC

```bash
# 删除由RC创建的pods
kubectl delete rc kubia 
# 保留由RC创建的pods
kubectl delete rc kubia --cascade=false 
```

### RS

- RS和RC类似，只是在RC的基础上添加了更多的label selector 参数

```bash
vim kubia-rs.yaml 
# RS的apiVersion和RC不同
apiVersion: apps/v1beta2
kind: ReplicaSet
metadata:
  name: kubia
spec:
  replicas: 3
  selector:
    matchLabels:
      app: kubia
  template:
    metadata:
      labels:
        app: kubia
    spec:
      containers:
      - name: kubia
        image: luksa/kubia
# 创建RS
kubectl create -f kubia-rs.yaml
# 查看RS信息
kubectl get rs
# 查看pod会发现Kubernetes创建了三个新的pod并随机部署在node上面
kubectl get pods
# 删除RS，同时会删除由RS创建的pods
kubectl delete rs kubia
```

### DS

- DS与RC、RS类似，区别在于DS可以指定node节点

```bash
vim kubia-ds.yaml 
# 在RC、RS基础上添加了nodeSelector（需要设置node label）
apiVersion: apps/v1beta2
kind: DaemonSet
metadata:
  name: ssd-monitor
spec:
  selector:
    matchLabels:
      app: ssd-monitor
  template:
    metadata:
      labels:
        app: ssd-monitor
    spec:
      nodeSelector:
        disk: ssd
      containers:
      - name: main
        image: luksa/ssd-monitor
# 创建DS
kubectl create -f kubia-ds.yaml
# 查看DS信息
kubectl get ds
# 查看pod会发现Kubernetes在指定的node上面各创建了一个pod
kubectl get pods
# 如果没有查看到pod信息，请尝试为node添加label信息
kubectl label node vm06 disk=ssd 
# 将node移除DS只需要更改标签即可
kubectl label node vm06 disk=sss --overwrite
# 删除DS，同时会删除由DS创建的pods
kubectl delete rs kubia
```

## 实验三：使用Job实现任务的批量处理

- 串行完成任务的批量处理

```bash
vim multi-completion-batch-job.yaml 
# 五个任务将一个个执行
apiVersion: batch/v1
kind: Job
metadata:
  name: multi-completion-batch-job
spec:
  completions: 5
  template:
    metadata:
      labels:
        app: batch-job
    spec:
      restartPolicy: OnFailure
      containers:
      - name: main
        image: luksa/batch-job
```

- 并行完成任务的批量处理

```bash
vim multi-completion-parallel-batch-job.yaml 
# 添加parallelism参数，一次执行两个任务直至五个任务都完成
apiVersion: batch/v1
kind: Job
metadata:
  name: multi-completion-batch-job-parallel
spec:
  completions: 5
  parallelism: 2
  template:
    metadata:
      labels:
        app: batch-job
    spec:
      restartPolicy: OnFailure
      containers:
      - name: main
        image: luksa/batch-job
```

- 创建job、查看pods信息与上文一致

## 实验四：使用CronJob实现定时任务

- 创建定时任务

```bash
vim cronjob.yaml 
apiVersion: batch/v1beta1
kind: CronJob
metadata:
  name: batch-job-every-fifteen-minutes
spec:
  schedule: "0,15,30,45 * * * *"
  jobTemplate:
    spec:
      template:
        metadata:
          labels:
            app: periodic-batch-job
        spec:
          restartPolicy: OnFailure
          containers:
          - name: main
            image: luksa/batch-job
```

- schedule：分  时  日  月  周（如0,15,30,45 * * * * 表示每周每月每天每时每隔15分钟运行一次）