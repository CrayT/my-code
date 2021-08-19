## 云平台虚拟机管理API
### URL及功能描述
| METHOD | URI | BODY |  功能描述  | 
| ------ | --- | ---- |  -------- | 
| POST   | /vm/hosts | { create_id:{create_id},memory:{memory},cpu:{cpu},memory_mul:{memory_mul},cpu_mul:{cpu_mul},num:{num},ip:{ip},name:{name},description:{description}} | 新建宿主机 |
| GET    | /vm/hosts | | 返回宿主机列表（包含uid与名称及额度信息） |
| GET    | /vm/hosts/{host_uid} | | 返回某宿主机的基本信息（包含IP,创建人，创建时间，修改人，修改时间，内存，内存超分倍数，cou核数,cou核数超分倍数）及状态信息(是否开机,是否可用) |
| PUT    | /vm/hosts/{host_uid} | { update_id:{update_id},memory_mul:{memory_mul},cpu_mul:{cpu_mul},num:{num},name:{name},description:{description} } | 更新某宿主机信息|
| DELETE | /vm/hosts/{host_uid} | | 删除宿主机 |
| GET    | /vm/users | | 返回用户列表(包含uid及额度信息) |
| POST   | /vm/users/{user_uid} | { create_id:{create_id},memory:{memory},cpu:{cpu},num:{num} } | 新建用户 |
| GET    | /vm/users/{user_uid} | | 返回某用户信息（包含内存额度，已用内存，cpu额度，已用cpu，数量额度,已用数量，用户状态，创建人，创建时间，修改人，修改时间）|
| PUT    | /vm/users/{user_uid} | { update_id:{update_id},memory:{memory},cpu:{cpu},num:{num},state:{state}} | 更新某用户信息 |
| DELETE | /vm/users/{user_uid} | | 删除用户 |
| POST   | /vm/vms | { create_id:{create_id},memory:{memory},cpu:{cpu},system:{system},key:{key_uid},host:{host_uid}} | 新建虚拟机 |
| GET    | /vm/vms?user={user_uid} | | 返回某用户的虚拟机列表（包含虚拟机名称，虚拟机uid,配置信息,状态信息）,及该用户的额度信息 |
| GET    | /vm/vms?host={host_uid} | | 返回某宿主机上的虚拟机列表（包含虚拟机名称，虚拟机uid,配置信息,状态信息）,及该宿主机的汇总信息 |
| GET    | /vm/vms/{vm_uid} | | 返回某虚拟机信息(包含虚拟机mac地址，ip地址，内存，cpu,核数，系统，所属用户uid，所在宿主机uid,创建人，创建时间，修改人，修改时间，虚拟机状态) |
| PUT    | /vm/vms/{vm_uid} | { memory:{memory},cpu:{cpu},system:{system},ucode:{ucode} } | 更新某虚拟机信息 |
| DELETE | /vm/vms/{vm_uid} | | 删除虚拟机 |
| POST   | /vm/keys | { create_id:{create_id},content:{content},name:{name}} | 新建公钥 |
| GET    | /vm/keys?user={user_uid} | | 返回某用户公钥列表（包含公钥uid，公钥别名,公钥内容） |
| GET    | /vm/keys/{key_uid} | | 返回某公钥信息（包括公钥内容，创建人，创建时间） |
| DELETE | /vm/keys/{key_uid} | | 删除公钥 |
| POST   | /vm/systems | { create_id:{create_id},path:{path},name:{name}} | 新建系统 |
| GET    | /vm/systems | | 返回操作系统列表（包含系统名称，系统uid） |
| GET    | /vm/systems/{systems_uid} | | 返回某操作系统信息(包含路劲,创建人，创建时间，修改人，修改时间) |
| PUT    | /vm/systems/{system_uid} | { update_id:{update_id},path:{path}} | 更新某操作系统信息 |
| DELETE | /vm/systems/{system_uid} | | 删除系统 |

### 通用的状态码及描述信息
```
    '400':'错误的请求',
    '404':'对象不存在',
    '410':'参数不匹配',
    '500':'服务器错误'
```

## 宿主机模块

### 新建宿主机

- POST /vm/hosts
- 请求示例

```json
{ 
    "create_id":"root1234",
    "memory":64,
    "cpu":16,
    "memory_mul":2,
    "cpu_mul":2,
    "num":60,
    "ip":"127.0.0.1",
    "name":"vmhost_main2",
    "description":"test"
}
```
- 响应示例

请求成功
```json
{
    "status": 200,
    "description": "宿主机创建成功",
    "data": {
        "uid": "qad2woLn",
        "name": "vmhost_main3",
        "description":"test",
        "memory": 64,
        "memory_mul": 2,
        "cpu": 16,
        "cpu_mul": 2,
        "num": 60,
        "ip": "10.0.0.0",
        "create_id": "root1234",
        "create_at": "2018-09-03 10:02:26",
        "update_id": null,
        "update_at": null,
        "alive": false
    },
    "summary": null
}
```
请求失败
```json
{
    "status": 400,
    "description": "该IP地址的宿主机已经注册",
    "data": null,
    "summary": null
}
```
description详细的描述了发生错误的原因，包括有`该IP地址的宿主机已经注册`、`该名字已存在`，或通用描述信息。

### 查看宿主机列表

- GET /vm/hosts
- 响应实例

请求成功
```json
{
    "status": 200,
    "description": "宿主机信息请求成功",
    "data": [
        {
            "uid": "GtbsRdC5",
            "name": "vmhost_main",
            "description":"",
            "memory": 64,
            "memory_mul": 2,
            "cpu": 16,
            "cpu_mul": 2,
            "num": 60,
            "ip": "172.17.0.1",
            "create_id": "root1234",
            "create_at": "2018-09-03 09:02:34",
            "update_id": null,
            "update_at": null,
            "cpu_used": 1,
            "memory_used": 1,
            "num_used": 1,
            "alive": true
        },
        {
            "uid": "3QE7RG8u",
            "name": "vmhost_main2",
            "description":"",
            "memory": 64,
            "memory_mul": 2,
            "cpu": 16,
            "cpu_mul": 2,
            "num": 60,
            "ip": "10.1.1.1",
            "create_id": "root1234",
            "create_at": "2018-09-03 09:26:18",
            "update_id": null,
            "update_at": null,
            "cpu_used": 0,
            "memory_used": 0,
            "num_used": 0,
            "alive": false
        }
    ],
    "summary": null
}
```
### 查看特定宿主机
- GET /vm/hosts/GtbsRdC5
- 响应示例

成功示例
```json
{
    "status": 200,
    "description": "宿主机信息请求成功",
    "data": {
        "uid": "GtbsRdC5",
        "name": "vmhost_main",
        "description":"",
        "memory": 64,
        "memory_mul": 2,
        "cpu": 16,
        "cpu_mul": 2,
        "num": 60,
        "ip": "172.17.0.1",
        "create_id": "root1234",
        "create_at": "2018-09-03 09:02:34",
        "update_id": null,
        "update_at": null,
        "cpu_used": 1,
        "memory_used": 1,
        "num_used": 1,
        "alive": true
    },
    "summary": null
}
```
失败示例
```json
{
    "status": 404,
    "description": "对象不存在",
    "data": null,
    "summary": null
}
```

### 更新宿主机
- PUT vm/hosts/GtbsRdC5
- 请求示例

> 宿主机更新操作中必选字段是`update_id`，可选字段是`memory_mul`、`cpu_mul`、`num`、`name`、`description`

```json
{
	"update_id":"ud_admin",
	"memory_mul":3,
	"cpu_mul":3,
	"num":80,
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "宿主机更新成功",
    "data": {
        "uid": "GtbsRdC5",
        "name": "vmhost_main",
        "description":"",
        "memory": 64,
        "memory_mul": 3,
        "cpu": 16,
        "cpu_mul": 3,
        "num": 80,
        "ip": "172.17.0.1",
        "create_id": "root1234",
        "create_at": "2018-09-03 09:02:34",
        "update_id": "ud_admin",
        "update_at": "2018-09-03 02:39:50"
    },
    "summary": null
}
```

### 删除宿主机

- DELETE /vm/hosts/qad2woLn
- 响应实例

```json
{
    "status": 200,
    "description": "宿主机删除成功",
    "data": null,
    "summary": null
}
```
## 用户模块

### 新建用户
- POST /vm/users/thisidce
- 请求示例

```json
{ 
    "create_id":"root1234",
    "memory":20,
    "cpu":20,
    "num":8 
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "用户创建成功",
    "data": {
        "uid": "thisidce",
        "memory": 20,
        "cpu": 20,
        "num": 8,
        "state": "0",
        "create_id": "root1234",
        "create_at": "2018-09-03 10:56:01",
        "update_id": null,
        "update_at": null
    },
    "summary": null
}
```
### 查看用户列表
- GET /vm/users
- 响应示例

```json
{
    "status": 200,
    "description": "用户信息请求成功",
    "data": [
        {
            "uid": "asdfzxcv",
            "memory": 20,
            "cpu": 10,
            "num": 5,
            "state": "0",
            "create_id": "root1234",
            "create_at": "2018-08-29 13:55:29",
            "update_id": "root1234",
            "update_at": "2018-08-29 13:55:48",
            "cpu_used": 1,
            "memory_used": 1,
            "num_used": 1
        },
        {
            "uid": "thisidce",
            "memory": 20,
            "cpu": 20,
            "num": 8,
            "state": "0",
            "create_id": "root1234",
            "create_at": "2018-09-03 10:56:01",
            "update_id": null,
            "update_at": null,
            "cpu_used": 0,
            "memory_used": 0,
            "num_used": 0
        }
    ],
    "summary": null
}
```

### 查看特定用户
- GET vm/users/thisidce
- 响应示例

```json
{
    "status": 200,
    "description": "用户信息请求成功",
    "data": {
        "uid": "thisidce",
        "memory": 20,
        "cpu": 20,
        "num": 8,
        "state": "0",
        "create_id": "root1234",
        "create_at": "2018-09-03 10:56:01",
        "update_id": null,
        "update_at": null,
        "cpu_used": 0,
        "memory_used": 0,
        "num_used": 0
    },
    "summary": null
}
```

### 更新用户信息
- PUT /vm/users/thisidce
- 请求示例

> 用户更新操作必选字段是`update_id`,可选字段是`memory`、`cpu`、`num`

```json
{ 
    "update_id":"root1234",
    "memory":20,
    "cpu":30,
    "num":9 
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "用户信息更新成功",
    "data": {
        "uid": "thisidce",
        "memory": 20,
        "cpu": 30,
        "num": 9,
        "state": "0",
        "create_id": "root1234",
        "create_at": "2018-09-03 10:56:01",
        "update_id": "root1234",
        "update_at": "2018-09-03 03:45:38"
    },
    "summary": null
}
```
### 删除用户
- DELETE vm/users/qwertyui
- 响应示例

```json
{
    "status": 200,
    "description": "用户删除成功",
    "data": null,
    "summary": null
}
```
## 公钥模块

### 新建公钥
- POST /vm/keys
- 请求示例

```json
{ 
    "create_id":"asdfzxcv",
    "content":"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe3zdqM9jIvKn0iGHisd1pSNyEIHv4c+997zlDmxeLBr5HiXdjE1VfuNteoeRSRIuqkUNmJVgfSVA55cOdqGcfwsFJE+Zm2y9YqRefbPmIiQ1eAWqxyx843WuJHzMm8/x4d6M/AJ5PvhidGLpVLe/DhqUnCwa0L1ojhD9o1gkm1RIDyHxjIxzGOpLHC8ZlyXy6ys/DIRZyoEqmyFsSUMW/EV7wDmWpBgx6VN3a2P5N20D0neIf9gLzsZ0Ccxv6SguDAIpwIyX/fUgaOB26vwpjP7b0cYqkGOTcwB9QjI2PaLi6gHnImK3c3kq6tajjpactyEcQ1zEFbXQaTbQnOIxwB/kRoY0k2YyCXecQdynCKAfSrATO0G5Bt7nc1lqVBepSQcPnuOejswlpqUTYnLpAl+V9SD5ILQgP9B0ZgKJBdOR+JmxhXJPFEtjLM0tBeR5cvtJSe3gYpOuZpcFRp0twtPWKi/CZ0tuohKbx54Y1G3j1MWaAoCaUnl2LsYvR2+NyWZuQwRGSeErakxSfPKpANAb7UpQGefAQ7A3RgbsIipMO8ib8qOpiekgOR0GJNKHK235IV3pdZ4wb/HBmn0ESUsr2YZiGSIiAqQfbXK9HFMqzCR0+PBEITl0QcdtHoo0FpKiHK5OUXmtEZk4eQOuHbxQS9N5+tefZCgHyjoS7ew== guozhitingly@126.cn",
    "name":"demo3"
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "公钥创建成功",
    "data": {
        "uid": "XniTAc78",
        "name": "demo3",
        "content": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe3zdqM9jIvKn0iGHisd1pSNyEIHv4c+997zlDmxeLBr5HiXdjE1VfuNteoeRSRIuqkUNmJVgfSVA55cOdqGcfwsFJE+Zm2y9YqRefbPmIiQ1eAWqxyx843WuJHzMm8/x4d6M/AJ5PvhidGLpVLe/DhqUnCwa0L1ojhD9o1gkm1RIDyHxjIxzGOpLHC8ZlyXy6ys/DIRZyoEqmyFsSUMW/EV7wDmWpBgx6VN3a2P5N20D0neIf9gLzsZ0Ccxv6SguDAIpwIyX/fUgaOB26vwpjP7b0cYqkGOTcwB9QjI2PaLi6gHnImK3c3kq6tajjpactyEcQ1zEFbXQaTbQnOIxwB/kRoY0k2YyCXecQdynCKAfSrATO0G5Bt7nc1lqVBepSQcPnuOejswlpqUTYnLpAl+V9SD5ILQgP9B0ZgKJBdOR+JmxhXJPFEtjLM0tBeR5cvtJSe3gYpOuZpcFRp0twtPWKi/CZ0tuohKbx54Y1G3j1MWaAoCaUnl2LsYvR2+NyWZuQwRGSeErakxSfPKpANAb7UpQGefAQ7A3RgbsIipMO8ib8qOpiekgOR0GJNKHK235IV3pdZ4wb/HBmn0ESUsr2YZiGSIiAqQfbXK9HFMqzCR0+PBEITl0QcdtHoo0FpKiHK5OUXmtEZk4eQOuHbxQS9N5+tefZCgHyjoS7ew== guozhitingly@126.cn",
        "create_id": "asdfzxcv",
        "create_at": "2018-09-03 11:52:01"
    },
    "summary": null
}
```
### 查看某用户公钥列表
- GET /vm/keys?user=asdfzxcv
- 响应示例

```json
{
    "status": 200,
    "description": "公钥信息请求成功",
    "data": [
        {
            "uid": "XbTw7jSN",
            "name": "demo2",
            "content": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe3zdqM9jIvKn0iGHisd1pSNyEIHv4c+997zlDmxeLBr5HiXdjE1VfuNteoeRSRIuqkUNmJVgfSVA55cOdqGcfwsFJE+Zm2y9YqRefbPmIiQ1eAWqxyx843WuJHzMm8/x4d6M/AJ5PvhidGLpVLe/DhqUnCwa0L1ojhD9o1gkm1RIDyHxjIxzGOpLHC8ZlyXy6ys/DIRZyoEqmyFsSUMW/EV7wDmWpBgx6VN3a2P5N20D0neIf9gLzsZ0Ccxv6SguDAIpwIyX/fUgaOB26vwpjP7b0cYqkGOTcwB9QjI2PaLi6gHnImK3c3kq6tajjpactyEcQ1zEFbXQaTbQnOIxwB/kRoY0k2YyCXecQdynCKAfSrATO0G5Bt7nc1lqVBepSQcPnuOejswlpqUTYnLpAl+V9SD5ILQgP9B0ZgKJBdOR+JmxhXJPFEtjLM0tBeR5cvtJSe3gYpOuZpcFRp0twtPWKi/CZ0tuohKbx54Y1G3j1MWaAoCaUnl2LsYvR2+NyWZuQwRGSeErakxSfPKpANAb7UpQGefAQ7A3RgbsIipMO8ib8qOpiekgOR0GJNKHK235IV3pdZ4wb/HBmn0ESUsr2YZiGSIiAqQfbXK9HFMqzCR0+PBEITl0QcdtHoo0FpKiHK5OUXmtEZk4eQOuHbxQS9N5+tefZCgHyjoS7ew== guozhitingly@126.cn",
            "create_id": "asdfzxcv",
            "create_at": "2018-09-03 09:03:38"
        },
        {
            "uid": "XniTAc78",
            "name": "demo3",
            "content": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe3zdqM9jIvKn0iGHisd1pSNyEIHv4c+997zlDmxeLBr5HiXdjE1VfuNteoeRSRIuqkUNmJVgfSVA55cOdqGcfwsFJE+Zm2y9YqRefbPmIiQ1eAWqxyx843WuJHzMm8/x4d6M/AJ5PvhidGLpVLe/DhqUnCwa0L1ojhD9o1gkm1RIDyHxjIxzGOpLHC8ZlyXy6ys/DIRZyoEqmyFsSUMW/EV7wDmWpBgx6VN3a2P5N20D0neIf9gLzsZ0Ccxv6SguDAIpwIyX/fUgaOB26vwpjP7b0cYqkGOTcwB9QjI2PaLi6gHnImK3c3kq6tajjpactyEcQ1zEFbXQaTbQnOIxwB/kRoY0k2YyCXecQdynCKAfSrATO0G5Bt7nc1lqVBepSQcPnuOejswlpqUTYnLpAl+V9SD5ILQgP9B0ZgKJBdOR+JmxhXJPFEtjLM0tBeR5cvtJSe3gYpOuZpcFRp0twtPWKi/CZ0tuohKbx54Y1G3j1MWaAoCaUnl2LsYvR2+NyWZuQwRGSeErakxSfPKpANAb7UpQGefAQ7A3RgbsIipMO8ib8qOpiekgOR0GJNKHK235IV3pdZ4wb/HBmn0ESUsr2YZiGSIiAqQfbXK9HFMqzCR0+PBEITl0QcdtHoo0FpKiHK5OUXmtEZk4eQOuHbxQS9N5+tefZCgHyjoS7ew== guozhitingly@126.cn",
            "create_id": "asdfzxcv",
            "create_at": "2018-09-03 11:52:01"
        }
    ],
    "summary": null
}
```

### 查看特定公钥信息
- GET /vm/keys/XbTw7jSN
- 响应示例

```json
{
    "status": 200,
    "description": "公钥信息请求成功",
    "data": {
        "uid": "XbTw7jSN",
        "name": "demo2",
        "content": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDe3zdqM9jIvKn0iGHisd1pSNyEIHv4c+997zlDmxeLBr5HiXdjE1VfuNteoeRSRIuqkUNmJVgfSVA55cOdqGcfwsFJE+Zm2y9YqRefbPmIiQ1eAWqxyx843WuJHzMm8/x4d6M/AJ5PvhidGLpVLe/DhqUnCwa0L1ojhD9o1gkm1RIDyHxjIxzGOpLHC8ZlyXy6ys/DIRZyoEqmyFsSUMW/EV7wDmWpBgx6VN3a2P5N20D0neIf9gLzsZ0Ccxv6SguDAIpwIyX/fUgaOB26vwpjP7b0cYqkGOTcwB9QjI2PaLi6gHnImK3c3kq6tajjpactyEcQ1zEFbXQaTbQnOIxwB/kRoY0k2YyCXecQdynCKAfSrATO0G5Bt7nc1lqVBepSQcPnuOejswlpqUTYnLpAl+V9SD5ILQgP9B0ZgKJBdOR+JmxhXJPFEtjLM0tBeR5cvtJSe3gYpOuZpcFRp0twtPWKi/CZ0tuohKbx54Y1G3j1MWaAoCaUnl2LsYvR2+NyWZuQwRGSeErakxSfPKpANAb7UpQGefAQ7A3RgbsIipMO8ib8qOpiekgOR0GJNKHK235IV3pdZ4wb/HBmn0ESUsr2YZiGSIiAqQfbXK9HFMqzCR0+PBEITl0QcdtHoo0FpKiHK5OUXmtEZk4eQOuHbxQS9N5+tefZCgHyjoS7ew== guozhitingly@126.cn",
        "create_id": "asdfzxcv",
        "create_at": "2018-09-03 09:03:38"
    },
    "summary": null
}
```

### 删除公钥
- DELETE /vm/keys/XbTw7jSN
- 响应示例

```json
{
    "status": 200,
    "description": "公钥删除成功",
    "data": null,
    "summary": null
}
```

## 系统模块

### 新建系统
- POST /vm/systems
- 请求示例

```json
{ 
    "create_id":"root1234",
    "path":"/home/snowly/Documents/iso/ubuntucloud.qcow2",
    "name":"ubuntu",
    "type":"ubuntu"
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "系统创建成功",
    "data": {
        "uid": "nkxFPLgX",
        "name": "ubuntu",
        "path": "/home/snowly/Documents/iso/ubuntucloud.qcow2",
        "type": "ubuntu",
        "create_id": "root1234",
        "create_at": "2018-09-03 11:58:42",
        "update_id": null,
        "update_at": null
    },
    "summary": null
}
```

### 查看系统列表
- GET /vm/systems
- 响应示例

```json
{
    "status": 200,
    "description": "系统信息请求成功",
    "data": [
        {
            "uid": "dKPCFhJa",
            "name": "centos",
            "path": "/home/snowly/Documents/iso/centoscloud.qcow2",
            "type": "centos",
            "create_id": "root1234",
            "create_at": "2018-09-03 09:04:01",
            "update_id": null,
            "update_at": null
        },
        {
            "uid": "nkxFPLgX",
            "name": "ubuntu",
            "path": "/home/snowly/Documents/iso/ubuntucloud.qcow2",
            "type": "ubuntu",
            "create_id": "root1234",
            "create_at": "2018-09-03 11:58:42",
            "update_id": null,
            "update_at": null
        }
    ],
    "summary": null
}
```

### 查看特定系统
- GET /vm/systems/dKPCFhJa
- 响应示例

```json
{
    "status": 200,
    "description": "系统信息请求成功",
    "data": {
        "uid": "dKPCFhJa",
        "name": "centos",
        "path": "/home/snowly/Documents/iso/centoscloud.qcow2",
        "type": "centos",
        "create_id": "root1234",
        "create_at": "2018-09-03 09:04:01",
        "update_id": null,
        "update_at": null
    },
    "summary": null
}
```
### 更新系统信息
- PUT /vm/systems/dKPCFhJa
- 请求示例

> 跟新系统操作中必选字段是`update_id`，可选字段是`path`、`name`、`type`

```json
{ 
    "update_id":"root1234",
    "path":"/home/snowly/Documents/iso/ubuntucloud.qcow2",
    "name":"ubuntu18.04",
    "type":"ubuntu"
}
```
- 响应示例

```json
{
    "status": 200,
    "description": "系统更新成功",
    "data": {
        "uid": "dKPCFhJa",
        "name": "ubuntu18.04",
        "path": "/home/snowly/Documents/iso/ubuntucloud.qcow2",
        "type": "ubuntu",
        "create_id": "root1234",
        "create_at": "2018-09-03 09:04:01",
        "update_id": "root1234",
        "update_at": "2018-09-03 04:09:04"
    },
    "summary": null
}
```
### 删除系统
- DELETE /systems/nkxFPLgX
- 响应示例

```json
{
    "status": 200,
    "description": "系统删除成功",
    "data": null,
    "summary": null
}
```

## 虚拟机模块

### 新建虚拟机
- POST 
- 请求示例

```json
{ 
    "create_id":"asdfzxcv",
    "memory":1,
    "cpu":1,
    "system":"dKPCFhJa",
    "key":"XniTAc78",
    "host":"GtbsRdC5",
    "name":"vm_test9"
}
```
- 响应示例

请求成功

```json
{
    "status": 200,
    "description": "虚拟机创建成功",
    "data": {
        "uid": "tWRy85fg",
        "name": "vm_test",
        "mac": "52:54:00:c9:01:02",
        "key": "XniTAc78",
        "memory": 1,
        "cpu": 1,
        "system": "dKPCFhJa",
        "host": "GtbsRdC5",
        "create_id": "asdfzxcv",
        "create_at": "2018-09-03 12:36:05",
        "is_delete": false,
        "alive": true
    },
    "summary": null
}
```
请求失败

```json
{
    "status": 400,
    "description": "该系统不存在",
    "data": null,
    "summary": null
}
```

> 请求失败的错误描述包括`该用户不存在`、`该宿主机不存在`、`该公钥不存在`、`该系统不存在`、`该虚拟机名称已存在`、`该宿主机额度不足以分配新虚拟机`、
`该用户额度不足以分配新虚拟机`，以及其他通用状态描述。

### 根据条件查看虚拟机列表
- GET /vm/vms?user=asdfzxcv&host=GtbsRdC5

> 请求链接的两个参数均为可选参数

- 响应示例

```json
{
    "status": 200,
    "description": "虚拟机信息请求成功",
    "data": [
        {
            "uid": "anK8yT7Y",
            "name": "vm_test3",
            "mac": "52:54:00:c9:01:01",
            "key": "XbTw7jSN",
            "memory": 1,
            "cpu": 1,
            "system": "dKPCFhJa",
            "host": "GtbsRdC5",
            "create_id": "asdfzxcv",
            "create_at": "2018-09-03 09:06:32",
            "is_delete": false,
            "alive": true
        },
        {
            "uid": "tWRy85fg",
            "name": "vm_test",
            "mac": "52:54:00:c9:01:02",
            "key": "XniTAc78",
            "memory": 1,
            "cpu": 1,
            "system": "dKPCFhJa",
            "host": "GtbsRdC5",
            "create_id": "asdfzxcv",
            "create_at": "2018-09-03 12:36:05",
            "is_delete": false,
            "alive": true
        }
    ],
    "summary": null
}
```

### 查看特定虚拟机
- GET /vm/vms/anK8yT7Y
- 响应示例

```json
{
    "status": 200,
    "description": "虚拟机信息请求成功",
    "data": {
        "uid": "anK8yT7Y",
        "name": "vm_test3",
        "mac": "52:54:00:c9:01:01",
        "key": "XbTw7jSN",
        "memory": 1,
        "cpu": 1,
        "system": "dKPCFhJa",
        "host": "GtbsRdC5",
        "create_id": "asdfzxcv",
        "create_at": "2018-09-03 09:06:32",
        "is_delete": false,
        "alive": true,
        "ip": "192.168.101.101"
    },
    "summary": null
}
```
### 更新虚拟机
- PUT /vm/vms/tWRy85fg
- 请求示例

```json
{
	"ucode":1,
    "memory":8,
    "cpu":8,
    "system":"dKPCFhJa"
}
```

> 更新操作的必选参数是`ucode`，可选参数是`memory`、`cpu`、`system`，`ucode`不同取值对应不同操作类型，`0：重装系统，1：调额，2：重启，3：开机，4：重启`，可以根据`code`取值来提供合适的可选参数，若为提供则使用虚拟机当前的状态值

- 响应示例

```json
{
    "status": 200,
    "description": "虚拟机更新成功",
    "data": {
        "uid": "tWRy85fg",
        "name": "vm_test",
        "mac": "52:54:00:c9:01:02",
        "key": "XniTAc78",
        "memory": 8,
        "cpu": 8,
        "system": "dKPCFhJa",
        "host": "GtbsRdC5",
        "create_id": "asdfzxcv",
        "create_at": "2018-09-03 12:36:05",
        "is_delete": false,
        "alive": true,
        "ip": "192.168.101.102"
    },
    "summary": null
}
```

### 删除虚拟机
- DELETE /vm/vms/anK8yT7Y
- 响应示例

```json
{
    "status": 200,
    "description": "虚拟机删除成功",
    "data": null,
    "summary": null
}
```