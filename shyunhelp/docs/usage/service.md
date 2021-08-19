## 环境要求

- 已成功安装并配置Kubernetes集群
- 已用RC启动三个标签为app:kubia的pod

## 实验一 创建服务

- 利用已有的三个标签为kubia的pod创建服务kubia

```bash
vim kubia-svc.yaml
# 通过select选择app:kubia的pod
apiVersion: v1
kind: Service
metadata:
    name: kubia
spec:
    ports:
    - port: 80
      targetPort: 8080
    selector:
        app: kubia

# 创建服务
kubectl create -f kubia-svc.yaml

# 查看已启动服务服务
kubectl get svc

# 测试服务 需要修改pod名和服务ip
kubectl exec kubia-7nog1 -- curl -s http://10.111.249.153

# 通过服务名访问服务
kubectl exec kubia-7nog1 -- curl -s http:kubia
```

- 通过设定endpoint中的ip访问外部服务

```bash
# 自己本地启动一个minio服务
docker run -p 9001:9000 --name minio1 \
  -e "MINIO_ACCESS_KEY=AKIAIOSFODNN7EXAMPLE" \
  -e "MINIO_SECRET_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY" \
  -v /mnt/data:/data \
  -v /mnt/config:/root/.minio \
  minio/minio server /data

# 启动完成后可以在本地以ip：9001的方式访问
curl -s ip:9001

# 在集群内部访问你本地起的minio服务
vim external-service.yaml

# 创建一个服务，同时不指定标签，此时该服务没有一个pod
apiVersion: v1
kind: Service
metadata:
  name: external-service
spec:
  ports:
  - port: 80

kubectl create -f external-service.yaml

# 为external-service指定endpoints
vim external-service-endpoints.yaml

apiVersion: v1
kind: Endpoints
metadata:
  name: external-service
subsets:
  - addresses:
    - ip: <你的本地ip>
    ports:
    - port: 9001

kubectl create -f external-service-endpoints.yaml

# 创建完成后你就可以通过服务的ip或者域名访问到你本地的minio服务
kubectl exec <pod‘s name> -- curl external-service
```

- 通过域名访问外部服务

```bash
vim external-service-externalname.yaml

# 访问域名为www.frearb.com的服务
apiVersion: v1
kind: Service
metadata:
    name: external-service
spec:
    type: ExternalName
    externalName: www.frearb.com
    ports:
        - port: 80

# 创建服务，服务名为external-service
kubectl create -f external-service-externalname.yaml

# 通过服务名为external-service的服务访问域名为www.frearb.com的服务
kubectl exec kubia-7nog1 -- curl -s http://external-service
```

## 实验二 将服务暴露给外部客户端

- 创建可以在集群外部访问的服务

```bash
vim kubia-svc-nodeport.yaml
# 设置服务的类型为nodeport
apiVersion: v1
kind: Service
metadata:
    name: kubia-nodeport
spec:
    type: NodePort
    ports:
    - port: 80
        targetPort: 8080
        nodePort: 30123
    selector:
        app: kubia

kubectl create -f kubia-svc-nodeport.yaml

# 查看服务基本信息
kubectl get svc kubia-nodeport

# 在集群外部访问服务
- <1st node’s IP>:30123
```

- 通过ingress创建可以在外部访问的服务

```bash
# 首先需要确定kubenets是否开启ingress controller 判断是否有name为nginx-ingress-controller的pod
kubectl get po --all-namespaces

# 创建ingress controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/mandatory.yaml
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/master/deploy/provider/baremetal/service-nodeport.yaml

# 判断ingress controller安装完成
kubectl get pods -n ingress-nginx 
NAME                                       READY     STATUS    RESTARTS   AGE
default-http-backend-66b447d9cf-rrlf9      1/1       Running   0          12s
nginx-ingress-controller-fdcdcd6dd-vvpgs   1/1       Running   0          11s

vim kubia-ingress.yaml

# 将kubia.example.com域名指向kubia-nodeport服务
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
    name: kubia
spec:
    rules:
    - host: kubia.example.com
      http:
        paths:
        - path: /
          backend:
            serviceName: kubia-nodeport
            servicePort: 80

kubectl create -f kubia-ingress.yaml

# 将nginx-ingress-controller的ip写入/etc/hosts
kubectl get pods -o wide -n ingress-nginx

sudo vim /etc/hosts

#添加一条
<controller‘s ip>  kubia.example.com

#通过域名访问服务
curl http://kubia.example.com
```

##  实验三 判断一个pod是否准备好接受请求

```bash
# 修改rc的模板
kubectl edit rc kubia

# 添加一下内容
apiVersion: v1
...
spec:
  ...
  template:
  ...spec:
    ...containers:
    - name: kubia
      image: luksa/kubia
      readinessProbe:
        exec:
          command:
          - ls
          - /var/ready
    ...

# 删除所有pod并查看新启pod的ready状态
kubectl delete po --all
kubectl get pod

# 通过添加ready文件使pod状态为ready
kubectl exec <pod’s name> -- touch /var/ready
```

- 发现服务背后每一个pod的ip

```bash
vim kubia-svc-headless.yaml

# 创建一个headless服务
apiVersion: v1
kind: Service
metadata:
  name: kubia-headless
spec:
  clusterIP: None
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: kubia

kubectl create -f kubia-svc-headless.yaml
```

- 通过dns查找发现pod的ip

```bash
# 创建一个具有dns查找功能的pod
kubectl run dnsutils --image=tutum/dnsutils --generator=run-pod/v1 --command -- sleep infinity

# 查找kubia-headless背后pod的ip
kubectl exec dnsutils nslookup kubia-headless

# 查找kubia服务时，返回的是服务的cluster ip注意区别
kubectl exec dnsutils nslookup kubia
```