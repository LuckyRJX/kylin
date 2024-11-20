# 银河麒麟离线安装Docker



## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

### 安装方式

|  安装方式  | 版本号 |
| :--------: | :----: |
| 二进制安装 | 27.3.1 |

## 安装步骤

### 下载二进制包

```shell
下载地址：https://download.docker.com/linux/static/stable/x86_64/
清华镜像：https://mirror.tuna.tsinghua.edu.cn/docker-ce/linux/static/stable/x86_64/docker-27.3.1.tgz
```

### 卸载旧版本

```shell
sudo dnf remove docker docker-client docker-client-latest docker-common docker-latest  docker-latest-logrotate docker-logrotate docker-engine podman -y

```

### 解压安装

```shell
tar xzvf docker-27.*.*.tgz -C /opt
```

### 配置

```shell
 #直接复制二进制文件（第一种方式）
 sudo cp /opt/docker/* /usr/bin/
 #设置环境变量（第二种方式）
 echo 'export PATH=$PATH:/opt/docker' >> ~/.bash_profile
 source  ~/.bash_profile
#创建软件连接（第三种方式）
#循环/opt/docker下的文件创建（可以写脚本）
ls -n /opt/docker/docker /usr/bin/docker
```

### 配置文件

```shell
#registry-mirrors 填写能用
vim /etc/docker/daemon.json
{
   "registry-mirrors": [""]
}
```

### 启动

> 如果您需要使用其他选项启动守护进程，请修改上述内容 命令，或者创建并编辑文件以添加自定义配置选项。`/etc/docker/daemon.json`

```shell
#Docker 守护程序
sudo dockerd &
或
nohup dockerd >>/opt/docker/docker.log 2>&1 &
```

