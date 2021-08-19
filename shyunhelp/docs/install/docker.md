## 环境要求
- Ubuntu 16.04 Server LTS 版本
- 可以访问公网

## 安装 Docker

```bash
# 添加内部docker-ce源，并安装 docker-ce
sudo tee -a /etc/apt/sources.list.d/docker.list << EOF
    deb [arch=amd64] https://mirrors.dlcloud.info/docker-ce/linux/ubuntu/ xenial stable
EOF
sudo apt-key adv --keyserver=hkp://pgp.ustc.edu.cn --recv 7EA0A9C3F273FCD8
sudo apt update && sudo apt install -y docker-ce


# 打印docker服务信息，测试是否安装成功
sudo docker info

# 配置 当前普通用户进入docker组
sudo usermod -aG docker $(whoami) 

# 重新连接 ssh session 后可以不加sudo访问docker
docker info
```

## 配置 daocloud 加速器

```bash
# 使用daocloud一键配置
curl -sSL https://ftp.dlcloud.info/linuxsoftware/set_mirror.sh | sh -s https://docker.mirrors.ustc.edu.cn

# 重启docker后台服务使以上配置生效
sudo service docker restart
```

## 安装 docker-compose

```bash
# 首先确认是否安装python2、python3以及对应的pip管理工具
sudo apt install -y python-pip python3 python3-pip

# 配置pip至云平台pypi源，并升级pip
mkdir ~/.pip
tee ~/.pip/pip.conf << EOF
[global]
index-url=https://mirrors.dlcloud.info/pypi/simple
[list]
format=columns
EOF
sudo pip install -U pip
sudo pip3 install -U pip

# 安装 docker-compose
sudo pip3 install docker-compose
```