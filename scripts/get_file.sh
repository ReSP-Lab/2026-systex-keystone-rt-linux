#!/usr/bin/expect -f

set timeout 60
set keystone_ip 192.168.1.160
set password sifive
set filename clocks.csv

spawn scp -o StrictHostKeyChecking=no root@$keystone_ip:/root/$filename /home/oscar/Cyberlab/Sources/PhD/Codes/keystone-for-real-time-system/$filename
expect "password: "
send "$password\r"
expect eof