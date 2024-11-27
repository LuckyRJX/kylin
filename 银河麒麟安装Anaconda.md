# 银河麒麟安装JumpServer

## 软件环境

### 操作系统环境

|          操作系统版本          | 操作系统架构 |
| :----------------------------: | :----------: |
| 银河麒麟服务器操作系统 V10 SP3 |    X86-64    |

## 安装Anaconda3

### 安装依赖

```shell
dnf install libXcomposite libXcursor libXi libXtst libXrandr alsa-lib mesa-libEGL libXdamage mesa-libGL libXScrnSaver -y
```

### 下载Anaconda

```sehll
curl -O https://repo.anaconda.com/archive/Anaconda3-2024.10-1-Linux-x86_64.sh
```

### 开始安装

```shell
bash ~/Anaconda3-2024.10-1-Linux-x86_64.sh

Ctrl+C 退出阅读

yes

#路径尽量复制粘贴
/opt/anaconda3
```

### 初始化

```shell
source /opt/anaconda3/bin/activate
conda init
```

### Conda操作

#### 创建环境

```shell
conda create -n python39 python=3.9.0
```

#### 激活环境

```shell
conda activate python39
```

#### 退出环境

```sehll
conda deactivate
```

#### 删除环境

```sehll
conda env remove --name myenv
```

