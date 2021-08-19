## 基本信息

镜像站位于校内网，不设置公网访问，校内地址为 https://mirrors.dlcloud.info 。本镜像站主要服务于多用途云平台的 KVM 虚拟化集群、Docker集群、科研代码编写依赖库，充分发挥本地存储和网络优势。其主要包含 Ubuntu 、 CentOS 、Pypi 、Rubygems 、 Maven 、 NPM  、Vscode 、Docker-ce 、 Docker Registry 、 zerotier 、 Nextcloud 、 Apache基金会所有项目。

## 使用帮助

### Ubuntu

```bash
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo tee -a /etc/apt/sources.list << EOF
deb https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short) main restricted universe multiverse
deb-src https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short) main restricted universe multiverse
deb https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-updates main restricted universe multiverse
deb-src https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-updates main restricted universe multiverse
deb https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-backports main restricted universe multiverse
deb-src https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-backports main restricted universe multiverse
deb https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-security main restricted universe multiverse
deb-src https://mirrors.dlcloud.info/ubuntu/ $(lsb_release -c --short)-security main restricted universe multiverse 
EOF
sudo apt update

```

### CentOS
修改 `/etc/yum/CentOS-Base.repo` 文件：
```
# CentOS-Base.repo
#
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the
# remarked out baseurl= line instead.
#
#

[base]
name=CentOS-$releasever - Base
#mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
baseurl=https://mirrors.dlcloud.info/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=https://mirrors.dlcloud.info/centos/RPM-GPG-KEY-CentOS-7

#released updates
[updates]
name=CentOS-$releasever - Updates
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
baseurl=https://mirrors.dlcloud.info/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=https://mirrors.dlcloud.info/centos/RPM-GPG-KEY-CentOS-7

#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
baseurl=https://mirrors.dlcloud.info/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=https://mirrors.dlcloud.info/centos/RPM-GPG-KEY-CentOS-7

#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
baseurl=https://mirrors.dlcloud.info/centos/$releasever/centosplus/$basearch/
gpgcheck=1
enabled=0
gpgkey=https://mirrors.dlcloud.info/centos/RPM-GPG-KEY-CentOS-7

```

### Pypi

```bash
mkdir ~/.pip
tee ~/.pip/pip.conf << EOF
[global]
index-url=https://mirrors.dlcloud.info/pypi/simple
[list]
format=columns
EOF
```

### Rubygems

```bash
gem sources  
gem sources --remove https://rubygems.org/  
gem sources -a https://mirrors.dlcloud.info/rubygems/ 
gem update --system

```

### NPM

在用户主目录下 `~/.npmrc` 中添加一行即可生效：

```bash
registry=https://registry.dlcloud.info/repository/npm/
```

### Maven

往 Maven 的全局配置文件 `setting.xml` 的 `mirrors` 节中添加以下内容;

```bash
<mirror>      
    <id>dlcloud</id>    
    <name>dlcloud</name>  
    <url>https://registry.dlcloud.info/repository/maven-public/</url>    
    <mirrorOf>*</mirrorOf>
</mirror> 
```

### Vscode

```bash
sudo tee -a /etc/apt/sources.list.d/vscode.list << EOF
deb [arch=amd64] https://mirrors.dlcloud.info/vscode stable main 
EOF
sudo apt-get update
sudo apt-get install code
```

### Docker-ce && Docker Registry

```bash
sudo tee -a /etc/apt/sources.list.d/docker.list << EOF
deb [arch=amd64] https://mirrors.dlcloud.info/docker-ce/linux/ubuntu/ xenial stable
EOF
sudo apt-key adv --keyserver=hkp://keyserver.ubuntu.com --recv 7EA0A9C3F273FCD8
sudo apt update
echo y | sudo apt install docker-ce
sudo usermod -aG docker $(whoami)
curl -sSL https://get.daocloud.io/daotools/set_mirror.sh | sh -s https://docker.dlcloud.info/
sudo service docker restart

```





### Nextcloud

详见 [Nextcloud使用](../usage/nextcloud/)




### Apache

下载地址为： https://mirrors.dlcloud.info/apache/


### zerotier

只包含 Linux 客户端

```bash
sudo tee -a /etc/apt/sources.list.d/zerotier.list << EOF
deb https://mirrors.dlcloud.info/zerotier/debian/xenial xenial main
EOF
sudo apt update
sudo apt install zerotier
```