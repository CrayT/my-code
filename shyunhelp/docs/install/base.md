## 环境要求

- Ubuntu 16.04 Server LTS


## 基础配置

### 设置sudo免密码

```bash
# 使当前用户以后sudo免密码
echo "$(whoami) ALL=(ALL) NOPASSWD : ALL" | sudo tee /etc/sudoers.d/nopasswd4sudo 
```

### 配置Ubuntu源

```bash
# 移除旧的源配置文件
sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak

# 新增新的配置文件
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

# 更新本地软件缓存
sudo apt update

# 安装基础软件
echo y | sudo apt install curl gcc g++ make build-essential python-pip python3 python3-pip vim speedometer htop language-pack-zh-hans wget tmux unzip zip rar unrar rinetd uuid openssh-server

```

!!! info "软件包名及对应功能介绍"
    主要介绍一些Ubuntu Server操作系统中常用的管理工具软件包以及对应的功能简要介绍。

| 软件包名称 | 功能 |
| :-----------: | :----- |
| curl | 获取某个链接指向的内容，不下载 |
| wget | 获取某个链接指向的内容，下载到本地 |
| gcc | Linux系统中的C语言编译器 |
| g++ | Linux系统中的C++语言编译器 |
| build-essential | 源码编译依赖库 |
| make | Make源码编译工具，多用于软件从源码安装到操作系统 |
| python-pip | python2的pip管理工具 |
| python-pip3 | python3的pip管理工具 |
| vim | 命令行中的神一样的文本编辑器 |
| speedometer | 终端环境下实时监控网速工具 |
| htop | 优于top工具的一款系统资源监控工具 |
| language-pack-zh-hans | 中文语言包，主要是为了在ssh客户端是中文语言环境下不报warnning，以及支持中文编码显示 |
| tmux | 一款后台任务管理工具，适合将任务放置在后台离线执行 |
| unzip zip | zip类型压缩的文件解压缩和压缩工具 |
| unrar rar | rar类型压缩的文件解压缩和压缩工具 |
| rinetd | 端口转发工具，配置文件在`/etc/rinetd.conf` |
| uuid | 系统级的唯一编码生成工具 |
| openssh-server | ssh服务软件，可在安装系统时选择安装 |

### 添加Git源

```bash
# 添加git源
sudo add-apt-repository ppa:git-core/ppa
sudo apt-get update

# 可选，切换到加速节点
sudo sed -i 's/ppa.launchpad.net/ppa.luish.cc/' /etc/apt/source.list.d/git.list
# 换回ppa源
sudo sed -i 's/ppa.luish.cc/ppa.launchpad.net/' /etc/apt/source.list.d/git.list

# 安装git
sudo apt install git
```

### 安装zsh
```bash
# 安装zsh
echo y | sudo apt install zsh

# 安装zsh主题，需输入用户密码
sh -c "$(curl -fsSL https://mirrors.dlcloud.info/ftp/linuxsoftware/oh-myzsh.sh)"

# 配置zsh识别通配符
tee -a .zshrc << EOF
setopt nonomatch
EOF
source .zshrc
```

### 安装zerotier

!!! info "简要介绍"
    **zerotier** 是一款SDN（软件定义网络）开源软件。 

    - 官网是 https://zerotier.com 
    - 镜像站点 https://mirrors.dlcloud.info/zerotier

```bash
# 添加源公钥到本地可信任列表
curl -fsSL https://mirrors.dlcloud.info/zerotier/contact@zerotier.com.gpg | sudo apt-key add -

# 新增源文件
sudo tee -a /etc/apt/sources.list.d/zerotier.list << EOF
deb [arch=amd64] https://mirrors.dlcloud.info/zerotier/debian/  $(lsb_release -cs) stable
EOF

# 更新本地软件列表缓存，并安装zerotier
sudo apt update
sudo apt install zerotier-cli

# 显示本地zerotier客户端id，并加入指定网络
sudo zerotier-cli status
sudo zerotier-cli join 网络号

```
