# 银河麒麟安装MySQL8

## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

### 安装方式

|   安装方式   |   版本号    |
| :----------: | :---------: |
| 源码编译安装 | Redis6.2.14 |

## 软件部署

### 源码编译安装

#### 下载源码包

> https://codeload.github.com/redis/redis/tar.gz/refs/tags/6.2.14

```shell
wget https://codeload.github.com/redis/redis/tar.gz/refs/tags/6.2.14 -O redis-6.2.14.tar.gz 
```

#### 解压

```shell
tar -xf redis-6.2.14.tar.gz
```

#### 编译安装

```shell
cd redis-6.2.14/deps/jemalloc
./configure
make dist
make && make install

cd ../../
make && make PREFIX=/opt/redis  install 
```

#### 配置文件

```shell
#配置文件在源码包里面，拷贝到redis安装目录下就可以了
daemonize yes #后台运行
```

#### 命令

```shell
/opt/redis/bin/redis-server /opt/redis/redis.conf
```

