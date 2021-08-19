## 环境要求
- 安装有`Docker 17.12`以上版本
- 安装有`docker-compose`工具

如未达到以上要求，请见[Docker安装指南](docker.md)。

## 安装Nextcloud

### 配置数据存储目录

```
sudo mkdir -p /home/data/lab/nextcloud
```

### 配置`docker-compose.yml`

```yaml
###docker-compose.yml
version: '2'

services:
  db:
    image: mariadb
    restart: always
    volumes:
      - /home/data/lab/nextcloud/db:/var/lib/mysql
    environment:
      - MYSQL_ROOT_PASSWORD=root
      - MYSQL_PASSWORD=nextcloud
      - MYSQL_DATABASE=nextcloud
      - MYSQL_USER=nextcloud

  app:  
    image: nextcloud
    ports:
      - 10080:80
    links:
      - db
    volumes:
      - /home/data/lab/nextcloud/www:/var/www/html
    restart: always
```

### 启动Nextcloud

```bash
#启动应用
sudo docker-compose up -d

#关闭应用
sudo docker-compose down
```

### 修改应用数据目录权限

```bash
# 进入app容器内部
sudo docker exec -ti nextcloud_app_1 /bin/bash

# 将应用目录赋权为 www-data 用户所有，否则在浏览器访问时会出现 503 错误
sudo chown -R www-data:www-data /var/www/html
```

启动应用后可以使用配置好的Nginx反向代理域名在浏览器中访问初始化，并设置好 **管理员账户** 和数据库服务器 **db** 。


### 其他配置

- 配置可访问域名：修改文件`www/config/config.php`

```php
'trusted_domains' => 
  array (
    0 => '127.0.0.1:10080',
    1 => 'yun.shyun.xyz',
  ),
```


## 备份恢复

### 备份

备份脚本`backup.sh`内容如下：

```bash
#! /bin/bash
time=`date +%Y-%m-%d_%H:%M:%S`
BACKDIR=/home/data/lab/backup     #存放目录

mkdir -p $BACKDIR
tar zcf $BACKDIR/nextcloud.$time.tar.gz /home/data/lab/nextcloud    #备份nextcloud文件夹
echo 'END!'

# 内容结束，以下命令给脚本文件赋予可执行权限
chmod +x backup.sh
```

### 恢复

使用上面提到的`docker-compose.yml`文件和备份解压出来的文件夹再次启动 **Nextcloud** 即可。

```bash
tar zxf nextcloud.$time.tar.gz 
sudo docker-compose up -d
```

### 添加可信任域名

其中 `0` 代表信任列表中的顺序
```bash
docker exec --user www-data  nextcloud_app_1 php occ config:system:set trusted_domains 0 --value=127.0.0.1:7009
```

### 取消重写到同一域名

```bash
docker exec --user www-data  nextcloud_app_1 php occ config:system:delete overwritehost
```