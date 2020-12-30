# Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for information about contributing to this project.

and describe any changes in the [change log](CHANGELOG.md).

### for Docker
If you make any changes, be sure to build a container to verify that it successfully completes:
```bash
docker build -t  .
```

# PMS PLUS WEB API

# Prerequisite

python3
mysql database and create scheme `pms_plus`

# Installation

install requirements locally
```bash
python3 -m pip install -r requires.txt
```

# Scheduler Tasks

票證
crontab/add-server-crontab/add-crontab-ticket_transaction_happycash.sh
crontab/add-server-crontab/add-crontab-ticket_transaction_icash.sh
crontab/add-server-crontab/add-crontab-ticket_transaction_ipass.sh
crontab/add-server-crontab/add-crontab-ticket_transaction_ecc.sh

定期票
crontab/./run-commutation.sh

PV3即時交易資料解析
crontab/./run-cron.sh

RSPMS
crontab/rspms/. run instant_transaction.sh
crontab/rspms/. run statistics_analysis.sh


## Installation on Windows 

forget about Windows ! use virtual machine instead, (windows 7 does not support docker too).
# Run Server

generic syntax

run server with default port 5000, default environment configuration file 'config/env.develop'
```bash
python3 main.py
```

init database and populate default value.
```bash
python3 main.py --db init
```

init database and populate demo value.
```bash
python3 main.py --demo
```


run server with custom environment file, following will read '/config/env.test'. Without specifying any --env arguments, server will load 'config/env.develop' by default
```bash
python3 main.py --env=test
```

run server with specified port
```bash
python3 main.py --port 8080
```

run server with specified backup db
account, pwd loading env.config
backup path will auto create if isn't exist
backup file_name will be db_name + datetime
```bash
python3 main.py --env=rspms --backup mysql pms_plus /home/pms_plus/backup
```




## For Maintainers

please follow PEP8 

# Production Note for CentOS7/ AWS Linux

# Python3
```
sudo yum groupinstall -y Development tools
sudo yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
```

download Python3 from official website and unzip it, then proceed the following compile steps.

```
sudo ./configure --prefix=/usr/local
sudo make
sudo make install
```

# Firewall
systemctl enable firewalld
systemctl start firewalld 
### Frontend angular
sudo firewall-cmd --zone=public --add-port=8080/tcp
## Backend python server
sudo firewall-cmd --zone=public --add-port=8000/tcp
## FTPs
sudo firewall-cmd --zone=public --add-port=21/tcp
#### FTPs Passive port
sudo firewall-cmd --zone=public --add-port=65400-65410/tcp

## MySQL

https://dptsource.blogspot.tw/2018/02/how-to-install-latest-mysql-579-on.html

## MONGO
use docer image
cmd: Docker pull mongo
mongo version: v4.0.1
volumes: /data/db

## Nginx
https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7

### Genreate SSL Key
sudo openssl req -x509 -nodes -days 3650 -newkey rsa:1024 -keyout /etc/vsftpd/private/vsftpd2.key -out /etc/vsftpd/public/vsfptd3.pem

### Sampel Configuration

```
#ray
pasv_enable=YES
pasv_max_port=65410
pasv_min_port=65400
pasv_address=192.168.0.201
#ssl
require_ssl_reuse=NO
implicit_ssl=NO
listen_port=21
ssl_enable=YES
allow_anon_ssl=NO
force_local_data_ssl=YES
force_local_logins_ssl=YES
ssl_ciphers=HIGH
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
rsa_cert_file=/etc/vsftpd/public/vsfptd3.pem
rsa_private_key_file=/etc/vsftpd/private/vsftpd2.key
```

# Server status

## ec2-user@ec2-54-245-162-118.us-west-2.compute.amazonaws.com

### 平板

#### dev site

/home/ec2-user/servers/pmsplus-server-pad-devel/./run-pad-devel.sh

#### demo site

### folder rule
目前票證交易檔上傳目錄
/home/pms_plus/pmsplus-server/csvs/in/ {customer_code} / {garage_code}

目前供下載票證交易檔黑名單目錄
(愛金卡)
/home/pms_plus/pmsplus-server/csvs/out/ {customer_code} / iCash.bl
(一卡通)
/home/pms_plus/pmsplus-server/csvs/out/ {customer_code} / iPass.bl
(遠鑫卡)
/home/pms_plus/pmsplus-server/csvs/out/ {customer_code} / happyCash.bl
(悠遊卡)
/home/pms_plus/pmsplus-server/csvs/out/ {customer_code} / ecc.bl

目前設計檔案目錄
/home/pms_plus/file_directory/
目前票證交易檔案處理目錄
/home/pms_plus/file_directory/ticket_transaction_files/ {customer_code} / {card_type} /

定期票上傳目錄
/home/pms_plus/pmsplus-server/csvs/in/{customer_code}/commutation_ticket

目前排程log目錄
/home/pms_plus/log/crontab/ticket_transaction/ {card_type} / 

RSPMS

/home/pms_plus/{projects}_fileserver/in/ {customer_code} / {garage_code} /



