# 银河麒麟安装MongoDB7

## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

### 安装方式

|  安装方式  |      版本号       |
| :--------: |:--------------:|
| 二进制安装 | MongoDB 7.0.15 |

## 软件部署

### 二进制安装

#### 安装依赖

```shell
sudo yum install libcurl openssl xz-libs -y
```

#### 下载包

```shell
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-rhel8-7.0.15.tgz
```

#### 创建 MongoDB 目录

```shell
sudo mkdir -p /opt/mongodb/{lib,log,run,mongosh}
```

#### 解压移动

```shell
tar -zxvf mongodb-linux-*-7.0.*.tgz
cp -r ./mongodb-linux-x86_64-rhel80-7.0.15/* /opt/mongodb/
```

#### 配置文件

```shell
vim /opt/mongodb/mongod.conf

# mongod.conf

storage:
  dbPath: /opt/mongodb/lib  # MongoDB 数据存储路径
systemLog:
  destination: file
  path: /opt/mongodb/log/mongod.log  # 日志文件路径
  logAppend: true  # 是否追加日志
net:
  port: 27017  # MongoDB 端口
  bindIp: 127.0.0.1  # 绑定的 IP 地址，修改为 0.0.0.0 以允许远程连接
processManagement:
  fork: true  # 是否以守护进程方式运行
  pidFilePath: /opt/mongodb/run/mongod.pid  # PID 文件路径

```

#### 命令

```shell
#启动
/opt/mongodb/bin/mongod -f /opt/mongodb/mongod.conf
#关闭
/opt/mongodb/bin/mongod  --shutdown  --dbpath /opt/mongodb/lib/
```

## 连接MongoDB

```shell
#下载
wget https://downloads.mongodb.com/compass/mongosh-2.3.3-linux-x64.tgz
#解压
tar -zxvf mongosh-*-linux-x64.tgz
#移动
cp -r ./mongosh-2.3.3-linux-x64/* /opt/mongodb/mongosh
#连接
/opt/mongodb/mongosh/bin/mongosh "mongodb://127.0.0.1:27017"
```

