## 环境要求
- `Gitlab Server` 版本更新到最新
- Ubuntu Server
- Docker 已安装

## 安装 gitlab-runner

采用 Docker 方式安装 gitlab-runner 不会因为使用多种编译环境造成主机环境污染，因此要求预先 Docker 。由于 `Gitlab Server` 与 gitlab-runner 之间通信只要求 gitlab-runner 能够到达 `Gitlab Server` 即可，所以任何一台内网机器都可以作为 gitlab-runner。

### 拉取镜像

```bash
docker pull gitlab/gitlab-runner:latest
```

### 启动容器

```bash
docker run -d --name gitlab-runner --restart always \
  -v /srv/gitlab-runner/config:/etc/gitlab-runner \
  -v /var/run/docker.sock:/var/run/docker.sock \
  gitlab/gitlab-runner:latest
```

## 配置 gitlab-runner

### 查看注册信息

通过访问 https://git.dlcloud.info/git/用户名/项目名/settings/ci_cd 查询注册 gitlab-runner 的 `URL` 和 `令牌` 。


### 注册 gitlab-runner

- 运行以下命令
```bash
docker exec -ti gitlab-runner gitlab-runner register
```
- 输入 `Gitlab Server` 的 URL 地址
```bash
Please enter the gitlab-ci coordinator URL (e.g. https://gitlab.com )
https://git.dlcloud.info
```
- 输入注册令牌
```bash
Please enter the gitlab-ci token for this runner
xxx
```
- 输入 gitlab-runner 的描述
```bash
Please enter the gitlab-ci description for this runner
[hostame] my-runner
```
- 输入与 gitlab-runner 相关联的标签（这个之后可以在 Gitlab 的 web 界面中修改）
```bash
Please enter the gitlab-ci tags for this runner (comma separated):
my-tag,another-tag
```
- 选择是否运行未加标签的任务
```bash
Whether to run untagged jobs [true/false]:
[false]: true
```
- 选择是否锁定 gitlab-runner 到当前的项目
```bash
Whether to lock Runner to current project [true/false]:
[true]: true
```
- 输入 runner 执行编译的方式（一般选择 Docker）
```bash
Please enter the executor: ssh, docker+machine, docker-ssh+machine, kubernetes, docker, parallels, virtualbox, docker-ssh, shell:
docker
```
- 输入默认的 docker 镜像（使用 ruby 可以编译 jekyll ）
```bash
Please enter the Docker image (eg. ruby:2.1):
ruby:2.1
```