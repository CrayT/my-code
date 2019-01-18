## 环境要求
- 三台 Ubuntu 虚拟机（16.04 或者 18.04）
- 配有上网 IPv4 和 IPv6 地址
- 可以使用 IPv6 地址访问 k8s.gcr.io (必要条件，否则无法从谷歌上安装软件和拉取镜像)
- 已安装 Docker 环境，未安装请见[Docker安装指南](docker.md)

## 环境准备

### 配置主机名对应

```bash
# 将三台虚拟机的内网IP和主机名对应写入 /etc/hosts 中
# 三台虚拟机均要配置
sudo tee -a /etc/hosts << EOF
192.168.112.104 vm04
192.168.112.105 vm05 
192.168.112.106 vm06 
EOF
```

## 配置 Kubernetes 源，并安装工具

```bash
curl -s "https://packages.cloud.google.com/apt/doc/apt-key.gpg" | sudo apt-key add -
sudo tee -a /etc/apt/sources.list.d/kubernetes.list << EOF
    deb https://apt.kubernetes.io/ kubernetes-$(lsb_release -c --short) main
EOF

export KUBE_VERSION="1.11.2"
sudo apt update && sudo apt install -y kubelet=${KUBE_VERSION}-00 kubeadm=${KUBE_VERSION}-00 kubectl=${KUBE_VERSION}-00
```


## 初始化配置和加入集群

```bash
# 执行初始化操作
sudo kubeadm init
# 初始化完成后可以看见以下命令提示以及node节点加入集群命令提示

# 为master节点配置管理配置文件
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

# 在node节点上加入集群
sudo kubeadm join 192.168.112.104:6443 --token i9mr2k.6uv14uu8cdem9a3x --discovery-token-ca-cert-hash sha256:2005aa069e585a5e4bcf275d9aa4b55439ff70f2a30cc869b43a785a6a2eafb7

# 获取节点状态
kubectl get node
# 到此处如果看见了所有节点处于Ready状态那就安装完成了
```

## 其他操作

###　重置配置

```bash
echo y | sudo kubeadm reset

sudo systemctl daemon-reload
sudo systemctl restart kubelet
```