# CentOS8配置DNS服务器

## 配置yum源

```shell
minorver=8.5.2111
sed -e "s|^mirrorlist=|#mirrorlist=|g" \
         -e "s|^#baseurl=http://mirror.centos.org/\$contentdir/\$releasever|baseurl=https://mirrors.aliyun.com/centos-vault/$minorver|g" \
         -i.bak \
         /etc/yum.repos.d/CentOS-*.repo
```

## 关闭防火墙

```shell
systemctl disable firewalld
systemctl stop firewalld
setenforce 0
sed -i s/SELINUX=enforcing/SELINUX=disabled/g /etc/selinux/config
```

## 下载软件

```sehll
yum install -y bind bind-chroot bind-utils
```

## 修改配置文件

### named.conf

```shell
sed -i "s/listen-on port 53 { 127.0.0.1; };/listen-on port 53 { any; };/g" /etc/named.conf
sed -i "s/allow-query     { localhost; };/allow-query     { any; };/g" /etc/named.conf

sed  -e "s/listen-on port 53 { 127.0.0.1; };/listen-on port 53 { any; };/g" \
	  -e "s/allow-query     { localhost; };/allow-query     { any; };/g" \
	  -i.bak \
	  /etc/named.conf


# vim /etc/named.conf
options {
        listen-on port 53 { 127.0.0.1; }; #127.0.0.1->any
        listen-on-v6 port 53 { ::1; };
        directory       "/var/named";
        dump-file       "/var/named/data/cache_dump.db";
        statistics-file "/var/named/data/named_stats.txt";
        memstatistics-file "/var/named/data/named_mem_stats.txt";
        secroots-file   "/var/named/data/named.secroots";
        recursing-file  "/var/named/data/named.recursing";
        allow-query     { localhost; }; #localhost->any
        recursion yes;
        dnssec-enable yes;
        dnssec-validation yes;
        managed-keys-directory "/var/named/dynamic";
        pid-file "/run/named/named.pid";
        session-keyfile "/run/named/session.key";
        include "/etc/crypto-policies/back-ends/bind.config";
};
```

### named.rfc1912.zones

> 大家配的时候还是要以常规域名后缀命名

```shell
#/etc/named.rfc1912.zones 
#备份
cp -r /etc/named.rfc1912.zones  /etc/named.rfc1912.zones.bak
cat >> /etc/named.rfc1912.zones  << EOF
zone "1314.xing" IN {
        type master;
        file "named.1314.xing";
        allow-update { none; };
};
zone "2.10.10.10.in-addr.arpa" IN {
        type master;
        file "10.10.10.in-addr.arpa";
        allow-update { none; };
};
EOF
```

###  正反向解析文件

> 多个域名就创建多份解析文件

```shell
touch /var/named/{named.1314.xing,10.10.10.in-addr.arpa}
chown -R root:named /var/named/{named.1314.xing,10.10.10.in-addr.arpa}

#正向 named.1314.xing
$TTL 1D
@	IN SOA	1314.xing. root.1314.xing. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
		NS	ns.1314.xing.
ns		IN A	10.10.10.2
@		IN A	10.10.10.2
www		IN A	10.10.10.2
vcs		IN A	10.10.10.1


#反向 10.10.10.in-addr.arpa

$TTL 1D
@	IN SOA	1314.xing. root.1314.xing. (
					0	; serial
					1D	; refresh
					1H	; retry
					1W	; expire
					3H )	; minimum
	NS	ns.1314.xing.
ns	A	10.10.10.2
2	PTR	1314.xing.
3	PTR	vcs.


#重启服务
systemctl restart named
```

### 修改本机网卡DNS

> 把本机网卡指向DNS 本机地址  10.10.10.2

```shell
vim /etc/sysconfig/network-scripts/ifcfg-ens33
sed -e "s|^DNS1=|#DNS1=|g" /etc/sysconfig/network-scripts/ifcfg-ens33
echo "DNS1=10.10.10.2" >> /etc/sysconfig/network-scripts/ifcfg-ens33
#重启网卡
nmcli c reload
nmcli c up ens33
systemctl restart NetworkManager
```

