# NEXTCLOUD

## API示例

包含的URL及其功能描述列表：

| Id   | URL                                 | Method | Description                                  | 完成 |
| ---- | ------------------------------------| ------ | -------------------------------------------- | :--: |
| 1    | /nextcloud/users                    | GET    | 返回所有用户的信息                              |  Y   |
| 2    | /nextcloud/users/create_id          | GET    | 返回特定用户的信息                              |  Y  |
| 3    | /nextcloud/users                    | POST | 创建待审核用户                                   |  Y   |
| 4    | /nextcloud/users/create_id          | PUT   | 审核是否创建用户                                 |  Y   |
| 5    | /nextcloud/users/create_id          | PUT    | 修改密码                                       |  Y   |
| 6    | /nextcloud/users/create_id          | DELETE | 根据create_id删除用户                          |  Y   |
| 7   | /nextcloud/users?username=           | GET     | 根据用户名查询用户是否存在                       |  Y   |


### 通用的状态码及描述信息
```
    '401':'user not exit',
    '402':'user exit',
    '403':'permission denied',
    '404':'sql error',
    '405':'illegal check_opinion'
```


	
### 根据create_id创建待审核用户
	
- POST /nextcloud/users

- 请求示例	

```json	
{
    "username":"gaofengz",
    "quota":"20",
    "create_id":"12345678",
    "comments":"test"
}
```

- 响应示例

> 若创建成功则返回200，若失败则返回400

请求成功：

```json
{
    "statuscode": "200",
    "message": "successfully post"
}	
```	
	
```	
{	
    "message": "illegal usrname",
    "statuscode": "400"
}
```

### 根据create_id审核用户，若审核通过则创建用户

- PUT /nextcloud/users/12345678

- 请求示例

```json
{
    "check_opinion":"1",
    "check_id":"00000000",
    "remarks":"permission"
}
```

- 响应示例

> 根据check_opinion判断是否创建用户

请求成功：

```json
{
    "statuscode": "202",
    "message": "user successfully create",
    "password": "MP0iExZ7"
}
```

请求失败：

```json
{
    "statuscode": "403",
    "message": "permission denied"
}
```

### 获取所有用户的账户信息

- GET /nextcloud/users

- 响应示例

> 返回nextcloud中的所有用户信息

```json
{	
            "uid": "QvSbpMGx",
            "username": "gaofengz",
            "quota": 20,
            "comments": "test",
            "create_id": "12345678",
            "create_at": "2018-09-03 07:39:35",
            "check_opinion": 1,
            "check_id": "00000000",
            "check_at": "2018-09-03 08:02:14",
            "remarks": "old_quota:20.0",
            "is_establish": true,
            "is_delete": false
        }
    ],
    "statuscode": "200"
}
```

### 获取特定用户的账户信息

- GET /nextcloud/users/12345678

- 响应示例

> 根据create_id返回特定用户信息

```json
{
    "statuscode": "200",
    "message": "OK",
    "data": [
        {
            "id": 1,
            "uid": "QvSbpMGx",
            "username": "gaofengz",
            "quota": 20,
            "comments": "test",
            "create_id": "12345678",
            "create_at": "2018-09-03 07:39:35",
            "check_opinion": 1,
            "check_id": "00000000",
            "check_at": "2018-09-03 08:02:14",
            "remarks": "old_quota:20.0",
            "is_establish": true,
            "is_delete": false
        }
    ]
}
```

### 修改某个用户的密码

- PUT /nextcloud/users/12345678

- 请求示例

```json
{
    "password":"asdfrewy234",
    "uid":"QvSbpMGx"
}
```

- 响应示例

> 返回密码修改是否成功

请求成功：
```json
{
    "statuscode": "204",
    "message": "password successfully modified"
}
```

请求失败：

```json
{
    "statuscode": "403",
    "message": "permission denied"
}
```

### 删除用户

- DELETE /nextcloud/users/12345678

- 响应示例

> 返回是否删除用户

```json
{
    "statuscode": "200"
}
```

### 判断用户是否存在

- GET /nextcloud/users?username=test

- 响应示例

用户存在：

```json
{
    "statuscode": "200",
    "message": "OK",
    "data": [
        {
            "comments": "qweq",
            "quota": 20,
            "create_id": "123456qz",
            "check_opinion": 1,
            "username": "test",
            "is_establish": true,
            "is_delete": false,
            "check_at": "2018-09-27 07:14:29",
            "uid": "qJbeikgM",
            "create_at": "2018-09-27 07:12:50",
            "remarks": "old_quota:20.0",
            "check_id": "12345678"
        }
    ]
}
```

请求失败：

```json
{
    "statuscode": "403",
    "message": "permission denied"
}
```