# 银河麒麟安装Nginx

## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

### 安装方式

|  安装方式  |     版本号      |
| :--------: |:------------:|
| 源码安装 | Nginx 1.26.2 |

## 软件部署

### 源码安装

#### 安装依赖

```shell
dnf install openssl -y
```

#### 下载源码包

```shell
wget https://nginx.org/download/nginx-1.26.2.tar.gz
```

#### 解压

```shell
tar -zxvf nginx-*.*.*.tar.gz
```

#### 创建用户和组

```shell
sudo groupadd nginx
sudo useradd nginx -g nginx -s /sbin/nologin -M
```

#### 编译安装

```shell
cd nginx1.26.2

mkdir -p /opt/nginx

./configure --prefix=/opt/nginx/ --user=nginx --group=nginx --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_gzip_static_module --with-http_sub_module --with-http_auth_request_module --with-http_random_index_module --with-http_secure_link_module --with-stream --with-stream_ssl_module --with-stream_realip_module --with-threads --with-file-aio --with-http_v2_module --with-cc-opt='-O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -m64 -mtune=generic -fPIC' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -pie'

make & make install
```

#### 命令

```shell
#启动
/opt/nginx/sbin/nginx
#启动，显示指定配置文件
/opt/nginx/sbin/nginx -t -c /opt/nginx/conf/nginx.conf

#重载
/opt/nginx/sbin/nginx -s reload

#快速停止
/opt/nginx/sbin/nginx -s stop
#有序退出
/opt/nginx/sbin/nginx -s quit
```

