#!/usr/bin/python
# coding:utf-8
import os
import subprocess

version="6.2.14"
port="6379"
password="123456"
download="/opt/download"
tar_dir="/opt/tar"
install_dir=f"/opt/redis-{version}"
download_url=f"https://codeload.github.com/redis/redis/tar.gz/refs/tags/{version}"

def install_redis():
    tmp = f"{download}/redis-{version}.tar.gz"
    if not os.path.exists(tmp):
        # 下载安装包
        exec_wget(download_url, download)
        subprocess.run(["mv", f"{download}/{version}", tmp])
    #解压安装包
    if not os.path.exists(f"{tar_dir}/redis-{version}"):
        exec_tar(tmp, tar_dir)

    os.chdir(f"{tar_dir}/redis-{version}/deps/jemalloc")
    subprocess.run(f"./configure")
    subprocess.run(["make","-C",f"{tar_dir}/redis-{version}/deps/jemalloc"])
    subprocess.run(["make","-C",f"{tar_dir}/redis-{version}/deps/jemalloc","install"])
    subprocess.run(["make", "-C", f"{tar_dir}/redis-{version}/deps/jemalloc", "dist"])
    if not os.path.exists(install_dir):
       subprocess.run(["make", "-C",f"{tar_dir}/redis-{version}"])
       subprocess.run(["make", "-C",f"{tar_dir}/redis-{version}",f"PREFIX={install_dir}","install"])
    subprocess.run(["cp",f"{tar_dir}/redis-{version}/redis.conf",f"{install_dir}/redis.conf"])

    f = open(f"{install_dir}/redis.conf", 'r+')
    flist = f.readlines()

    for i in range(len(flist)):
        if flist[i].startswith("port"):
            flist[i] = f'port {port}\n'
        if flist[i].startswith("daemonize"):
            flist[i] = f'daemonize yes\n'
        if flist[i].startswith("pidfile"):
            flist[i] = f'pidfile {install_dir}/redis.pid\n'
        if flist[i].startswith("# requirepass"):
            flist[i] = f'requirepass {password}\n'
    f = open(f'{install_dir}/redis.conf', 'w+')
    f.writelines(flist)
    f.close()
    os.chdir(os.getcwd())
    print(f"密码：{password}")
    print(f"启动命令：{install_dir}/bin/redis-server {install_dir}/redis.conf")
    print(f"关闭命令：{install_dir}/bin/redis-cli shutdown")
    print(f"关闭命令：{install_dir}/bin/redis-cli -h 127.0.0.1 -p {port} -a 123456")
    pass







#popen方式执行
def exec_popen(command):
    process = subprocess.Popen(command)
    # 等待进程完成并获取返回码
    return_code = process.wait()
    return return_code
#目录不存，在创建
def mkdir(path):  # path是指定文件夹路径
    if os.path.exists(path):
        print("目录已存在")
    else:
        os.makedirs(path)
        print(f"目录创建成功{path}")
#封装wget
def exec_wget(url,dir):
    command = ["sudo", "wget", url, "-P", dir, "--show-progress"]
    mkdir(dir)
    exec_popen(command)

def exec_tar(file,dir):
    command = ["sudo", "tar", "-xvf", file, "-C", dir]
    mkdir(dir)
    exec_popen(command)

if __name__ == "__main__":
    install_redis()
