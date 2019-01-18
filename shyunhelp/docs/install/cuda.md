## 环境要求

- 操作系统为`Ubuntu 16.04 Server`
- 已配置云平台Ubuntu源，未配置请见[基础配置指南](/install/base.md)

## 安装NVIDIA驱动

```bash
# 禁用Ubuntu自带第三方显卡驱动
sudo tee -a /etc/modprobe.d/blacklist-nouveau.conf << EOF
blacklist nouveau
options nouveau modeset=0
EOF
sudo update-initramfs -u
lsmod | grep nouveau   # 可以看见有内容

# 从Ubuntu源中安装nvidia驱动及其他依赖库
sudo apt install nvidia-384 mesa-common-dev freeglut3-dev

# 重启操作系统使内核禁用第三方驱动生效
sudo reboot
lsmod | grep nouveau   # 没有内容被打印
nvidia-smi             # 打印显卡信息
```

## 安装CUDA驱动

```bash
# 下载CUDA 9.0驱动
wget -c https://mirrors.dlcloud.info/ftp/linuxsoftware/cuda_9.0.run

# 执行安装，选择不再安装NVIDIA驱动，只安装CUDA Toolkit
sudo sh cuda.run --override

# 将CUDA 可执行文件目录和库文件目录加入到用户配置中

# zsh版本
tee -a ~/.zshrc << EOF
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64$LD_LIBRARY_PATH
EOF
source ~/.zshrc

# bash版本
tee -a ~/.bashrc << EOF
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64$LD_LIBRARY_PATH
EOF
source ~/.bashrc

```


## 安装NVIDIA-Docker工具

!!! note "注意"
    需要先安装Docker环境，如未安装请见[Docker安装](/install/docker.md)。凡是需要使用 **nvidia显卡** 的容器都需要使用 `nvidia-docker` 命令来启动，否则无法与显卡进行通信。

```bash
# 安装依赖库
sudo apt install nvidia-modprobe

# 下载nvidia-docker安装包
wget -c https://mirrors.dlcloud.info/ftp/linuxsoftware/nvidia-docker_1.0.1-1_amd64.deb

# 使用dpkg工具安装
sudo dpkg -i nvidia-docker_1.0.1-1_amd64.deb

# 使用nvidia-docker打印docker服务信息
sudo nvidia-docker info
```

## 其他问题解决
    
!!! question "问题一：问题描述"
    解决 **Driver/library version mismatch** ？

**问题分析** :这种问题主要是由于在更新了NVIDIA driver版本之后，系统内核中的版本没有更新，一般情况下重启服务器即可解决。此处需要讲在不进行重启服务器的情况下重载内核加载的模块版本。

```bash
# 查看当前加载的nvidia模块
lsmod | grep nvidia

# 返回的结果可能如下类似
nvidia_uvm            634880  8
nvidia_drm             53248  0
nvidia_modeset        790528  1 nvidia_drm
nvidia              12312576  86 nvidia_modeset,nvidia_uvm

# 先移除内核中nvidia驱动的依赖模块，在移除nvidia模块
sudo rmmod nvidia_drm
sudo rmmod nvidia_modeset
sudo rmmod nvidia_uvm
sudo rmmod nvidia

# 查看是否当前有进程正在使用nvidia驱动，如果有的话使用kill命令杀掉进程
sudo lsof /dev/nvidia*

# 查看当前加载的nvidia模块，应该不返回任何内容
lsmod | grep nvidia

# 使用以下命令确认正确返回nvidia显卡信息
nvidia-smi

#结束
```