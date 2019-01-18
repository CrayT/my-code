## 环境要求

- 已安装有最新版 `Docker` 环境

## 使用方法

校园内网访问地址：https://hub.dlcloud.info ，无校外访问地址。

浏览器访问可以通过登录访问，进行用户密码修改、新增仓库等操作。

该Docker私有镜像仓库基于 Harbor 搭建，只能进行私有镜像存储，如需使用Docker镜像源加速请转至 [加速源使用帮助](/usage/mirrors/#docker-ce-docker-registry)。

### 拉取镜像

#### 公开仓库

无须凭证，直接拉取镜像到本地即可。

```bash
docker pull hub.dlcloud.info/libraray/ubuntu:latest
```


#### 私有仓库

要求先登录生成 `Token` 才能有权限获取。

```bash
# 输入从管理员处获得的用户名和密码
➜  ~ docker login hub.dlcloud.info
Username: zhonger
Password: 
Login Succeeded
```

```bash
# 当返回登录成功时可以拉取镜像
docker pull hub.dlcloud.info/blcc/ubuntu:latest
```

### 推送镜像

推送镜像要求必须是对于命名空间有权限的用户才能进行。首先请使用 `docker login` 完成登录，登录成功之后如下操作：

```bash
docker tag ubuntu:latest hub.dlcloud.info/blcc/ubuntu:latest
docker push hub.dlcloud.info/blcc/ubuntu:latest
```