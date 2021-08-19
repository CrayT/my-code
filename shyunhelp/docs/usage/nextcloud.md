## 环境要求
- 适用于Linux、Mac、Windows、Android、IOS操作系统

## 在线使用

直接通过浏览器访问 URL 使用账号和密码即可登录使用，账号和密码、或者忘记密码请咨询管理员。

校内网地址： https://yun-i.dlcloud.info

公网地址： https://yun.dlcloud.info


## 客户端下载

### Mac、Windows用户
直接下载客户端安装包进行安装，以下为对应下载地址：

| 操作系统 | 下载地址 | 备注  |
| -- | -- | -- |
| Mac | https://mirrors.dlcloud.info/nextcloud/Mac | 校内网镜像 |
| Windows | https://mirrors.dlcloud.info/nextcloud/Windows | 校内网镜像 |
| Mac | https://download.nextcloud.com/desktop/releases/Mac/ | Nextcloud官网 |
| Windows | https://download.nextcloud.com/desktop/releases/Windows/ | Nextcloud官网 |



### Linux用户

- Ubuntu/Debian 用户

```bash
sudo tee -a /etc/apt/sources.list.d/nextcloud.list << EOF
deb http://ppa.launchpad.net/nextcloud-devs/client/ubuntu $(lsb_release -c --short) main 
deb-src http://ppa.launchpad.net/nextcloud-devs/client/ubuntu $(lsb_release -c --short) main 
EOF
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com --recv 1FCD77DD0DBEF5699AD2610160EE47FBAD3DD469
sudo apt update 
sudo apt install nextcloud-client
```

- Archlinux/openSUSE/Fedora 用户

直接在软件源中就可以安装 `nextcloud-client` 。

- Alpine Linux 用户

请移步至  https://pkgs.alpinelinux.org/packages?name=nextcloud-client

### Android用户

请在 Google Play 中搜索`nextcloud`下载，或者移步至官方下载 https://download.nextcloud.com/android/

### IOS用户

- APP Store 购买

花费1美元（6元人民币）购买 Nextcloud 客户端或者 Owncloud 客户端

- 免费使用

在 APP Store 中下载 Documents 通过添加 WebDav 的方式访问 Nextcloud 云盘。

## 客户端使用

### 一般客户端使用

服务器地址根据网络选择 在线使用 的 校内网地址 和 公网地址，账号和密码为预设，该方式主要用于远程与本地保持同步，可以自由设置远程目录与本地目录绑定同步，也可多目录分别同步。


### WebDav 方式使用

WebDav 地址如下所示，账号和密码和上面一致，该方式无须同步到本地。

| URL | 备注 |
| -- | -- |
| https://yun-i.dlcloud.info/remote.php/webdav | 校内地址 |
| https://yun.dlcloud.info/remote.php/webdav | 公网地址 |