# 银河麒麟安装MySQL8

## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

### 安装方式

|  安装方式  |    版本号    |
| :--------: | :----------: |
| 二进制安装 | MySQL 8.0.39 |

## 软件部署

### 二进制安装

> 安装mysql前卸载系统自带的mariadb

```bash
yum remove mariadb
```

### 检查C语言系统版本库

```shell
[root@learn-v10-sp3 ~]# getconf GNU_LIBC_VERSION
glibc 2.28
[root@learn-v10-sp3 ~]# ldd --version
ldd (GNU libc) 2.28
Copyright (C) 2018 自由软件基金会。
这是一个自由软件；请见源代码的授权条款。本软件不含任何没有担保；甚至不保证适销性
或者适合某些特殊目的。
由 Roland McGrath 和 Ulrich Drepper 编写。
```

### 下载二进制包

> 下载地址：https://downloads.mysql.com/archives/community/

```shell
https://cdn.mysql.com/archives/mysql-8.0/mysql-8.0.39-linux-glibc2.28-x86_64.tar.xz
```

### 解压

```shell
tar -xvf mysql-8.0.39-linux-glibc2.28-x86_64.tar.xz -C /opt
mv /opt/mysql-8.0.39-linux-glibc2.28-x86_64 /opt/mysql
chown root:root -R /opt/mysql
```



### 创建用户和用户组

```shell
groupadd mysql
useradd -r -g mysql mysql
```

### 配置文件

> 把配置文件放到安装目录下（/opt/mysql）

```shell
[mysql]
socket=/opt/mysql/run/socket.sock
[mysqld]
#基础设置
user=mysql
port=3306
basedir=/opt/mysql
datadir=/opt/mysql/data
socket=/opt/mysql/run/socket.sock
bind-address=0.0.0.0
lower_case_table_names=1
character-set-server=utf8mb4
collation-server=utf8mb4_general_ci

pid-file=/opt/mysql/run/mysqld.pid
log_error=/opt/mysql/log/error.log

# 启用二进制日志
server-id=1
log_bin=/opt/mysql/log/log_bin/mysql_bin
binlog_expire_logs_seconds=604800

# 开启慢查询日志
slow_query_log=ON
slow_query_log_file=/opt/mysql/log/mysql-slow.log
long_query_time=2

skip_name_resolve=1
#指的是事务等待获取资源等待的最长时间，超过这个时间还未分配到资源则会返回应用失败；
lock_wait_timeout = 3600
thread_stack = 512K
#当发生锁等待超时时，将回滚当前语句 (而不是整个事务)。要回滚整个事务，请使用“innodb_rollback_on_timeout” 开启值为：ON
innodb_rollback_on_timeout=ON
#back_log值指出在MySQL暂时停止回答新请求之前的短时间内多少个请求可以被存在堆栈中。也就是说，如果MySql的连接数达到max_connections时，新来的请求将会被存在堆栈中，以等待某一连接释放资源，该堆栈的数量即back_log，如果等待连接的数量超过back_log，将不被授予连接资源
back_log = 1024
#允许最大接收数据包的大小，防止服务器发送过大的数据包。
max_allowed_packet  = 1024M
#创建数据表时，默认使用的存储引擎
default_storage_engine = InnoDB 
character_set_server=utf8mb4
collation_server=utf8mb4_general_ci
key_buffer_size =2560M
#最大连接数，当前服务器允许多少并发连接。默认为 100，一般设置为小于 1000 即可。太高会导致内存占用过多，MySQL 服务器会卡死。作为参考，小型站设置 100 - 300
max_connections  = 512
#用户最大的连接数
max_user_connections = 200
#线程缓存，用于缓存空闲的线程。这个数表示可重新使用保存在缓存中的线程数，当对方断开连接时，如果缓存还有空间，那么客户端的线程就会被放到缓存中，以便提高系统性能。我们可根据物理内存来对这个值进行设置，对应规则
#    1G  ---> 8
#    2G  ---> 16
#    3G  ---> 32
#   >3G  ---> 64 
thread_cache_size=64


#MySQL 执行排序时，使用的缓存大小。增大这个缓存，提高 group by，order by 的执行速度。
sort_buffer_size=2M
#MySQL 读入缓存的大小。如果对表对顺序请求比较频繁对话，可通过增加该变量值以提高性能。
read_buffer_size=128k
#用于表的随机读取，读取时每个线程分配的缓存区大小。默认为 256k ，一般在 128 - 256k之间。在做 order by 排序操作时，会用到 read_rnd_buffer_size 空间来暂做缓冲空间。
read_rnd_buffer_size=256k
#程序中经常会出现一些两表或多表 Join （联表查询）的操作。为了减少参与 Join 连表的读取次数以提高性能，需要用到 Join Buffer 来协助 Join 完成操作。当 Join Buffer 太小时，MySQL 不会将它写入磁盘文件。和 sort_buffer_size 一样，此参数的内存分配也是每个连接独享。
join_buffer_size=128k
interactive_timeout = 600
bulk_insert_buffer_size = 64M
#HEAP 临时数据表的最大长度，超过这个长度的临时数据表 MySQL 可根据需求自动将基于内存的 HEAP 临时表改为基于硬盘的 MyISAM 表。我们可通过调整 tmp_table_size 的参数达到提高连接查询速度的效果。
tmp_table_size=32M

#read_only = 0
skip_replica_start = 0
#此变量控制LOAD DATA语句的服务器端LOCAL功能。根据local_infile设置，服务器会拒绝或允许 Client 端启用LOCAL的 Client 端加载本地数据。
log_replica_updates  = 1
#限制不使用文件描述符存储在缓存中的表定义的数量。
table_definition_cache=4000
#限制为所有线程在内存中打开的表数量。
table_open_cache=4000
log_timestamps = SYSTEM

#控制缓存表和索引数据的 InnoDB 缓冲池的内存大小
innodb_buffer_pool_size=3221225472
innodb_buffer_pool_instances = 8
#此为独立表空间模式，每个数据库的每个表都会生成一个数据空间。当删除或截断一个数据库表时，你也可以回收未使用的空间。这样配置的另一个好处是你可以将某些数据库表放在一个单独的存储设备。这可以大大提升你磁盘的I/O负载。
#独立表空间优点： 每个表都有自已独立的表空间。 每个表的数据和索引都会存在自已的表空间中。 可以实现单表在不同的数据库中移动。 空间可以回收（除drop table操作处，表空不能自已回收）
#缺点：单表增加过大，如超过100G
#结论：共享表空间在Insert操作上少有优势。其它都没独立表空间表现好。当启用独立表空间时，请合理调整：innodb_open_files
innodb_file_per_table=1 
#这个选项决定着什么时候把日志信息写入日志文件以及什么时候把这些文件物理地写(术语称为”同步”)到硬盘上。
#当设为 0 ,log buffer每秒就会被刷写日志文件到磁盘，提交事务的时候不做任何操作（执行是由mysql的master thread线程来执行的。
#当设为 1 时，每次提交事务的时候，都会将log buffer刷写到日志。
#当设为 2 ,每次提交事务都会写日志，但并不会执行刷的操作。每秒定时会刷到日志文件。要注意的是，并不能保证100%每秒一定都会刷到磁盘，这要取决于进程的调度。
innodb_flush_log_at_trx_commit = 2
#此参数确定些日志文件所用的内存大小，以M为单位。缓冲区更大能提高性能，但意外的故障将会丢失数据。事务日志所使用的缓存区。InnoDB在写事务日志的时候为了提高性能，先将信息写入Innodb Log Buffer中，当满足innodb_flush_log_trx_commit参数所设置的相应条件（或者日志缓冲区写满）时，再将日志写到文件（或者同步到磁盘）中。可以通过innodb_log_buffer_size参数设置其可以使用的最大内存空间。默认是8MB，一般为16～64MB即可。
innodb_log_buffer_size = 16M 
#事务日志文件写操作缓存区的最大长度。更大的设置可以提高性能，但也会增加恢复故障数据库所需的时间 Galera specific MySQL parameter default_storage_engine = InnoDB 服务器启动时必须启用默认存储引擎，否则服务器将无法启动。默认设置是 MyISAM。 这项设置还可以通过–default-table-type选项来设置。
innodb_redo_log_capacity=536870912
#数据包或生成的/中间的字符串的最大大小（以字节为单位）。
[client]
socket=/opt/mysql/run/socket.sock
```

### 创建目录

```shell
mkdir -p /opt/mysql/{run,log/log_bin,data}
chown -R mysql:mysql /opt/mysql/{run,log,data}
```



### 初始化数据库

> 不安全的初始化方式，初始化完之后密码是空，请及时修改

```shell
[root@learn-v10-sp3 opt]# /opt/mysql/bin/mysqld --defaults-file=/opt/mysql/my.cnf --initialize-insecure --user=mysql --basedir=/opt/mysql --datadir=/opt/mysql/data
```

### 启动

```shell
cp /opt/mysql/support-files/mysql.server /opt/mysql/
#修改mysql.server的46行和47行替换为
basedir=/opt/mysql
datadir=/opt/mysql/data



/opt/mysql/mysql.server start
/opt/mysql/mysql.server restart
/opt/mysql/mysql.server stop
#链接
/opt/mysql/bin/mysql --socket=/opt/mysql/run/socket.sock
#修改密码
/opt/mysql/bin/mysqladmin -uroot -p password 123456  --socket=/opt/mysql/run/socket.sock
```

