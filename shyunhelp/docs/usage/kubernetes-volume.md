## Volume的使用
### 环境要求：已经成功配置kubernetes集群。
#### 实验一：创建emptyDir类型的volume
- 在master节点创建一个包含两个pod的容器：fortune-pod.yaml，该实例为创建两个容器，volume挂载在pod内部的emptyDir中，达到共享访问数据的目的:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: fortune
spec:
  containers:
   - image: luksa/fortune
     name: html-generator
     volumeMounts:
      - name: html
        mountPath: /var/htdocs
   - image: nginx:alpine
     name: web-server
     volumeMounts:
       - name: html
         mountPath: /usr/share/nginx/html
         readOnly: true
     ports:
       - containerPort: 80
         protocol: TCP
  volumes:
   - name: html #通过名称引用volume
     emptyDir: {}
```
- 创建pod：
```
kubectl create -f
```
- 查看pod：
```
kubectl get pod
```

- 开启端口访问：
```
kubectl port-forward fortune 8080:80
```

- 通过8080端口获取nginx服务返回信息：
```
curl http://localhost:8080
```

#### 实验二 使用gitRepo作为volume
- 在master节点创建git-pod.yaml,该实例为创建pod时，volume类型为gitRepo，即创建后，在volume中clone git项目文件,该例子中，git包含html文件。

```yaml
apiVersion: v1
kind: Pod
metadata:
    name: gitrepo-volume-pod
spec:
   containers:
   - image: nginx:alpine
     name: web-server
     volumeMounts:
      - name: html
        mountPath: /usr/share/nginx/html
        readOnly: true
     ports:
       - containerPort: 80
         protocol: TCP
   volumes:
    - name: html
      gitRepo:
        repository: https://github.com/CrayT/kubia-website-example.git
        revision: master
        directory: .
```
- 创建pod：
```
kubectl create -f
```

- 查看pod：
```
kubectl get pod
```

- 开启端口访问：
```
kubectl port-forward gitrepo-volume-pod 8080:80
```

- 通过8080端口获取nginx服务返回信息：
```
curl http://localhost:8080
```
- 若git项目代码发生变化，不会立即体现在返回信息中，需要删除pod重新创建才会生效：
```
kubectl delete pod gitrepo-colume-pod
kubectl create -f git-pod.yaml
```