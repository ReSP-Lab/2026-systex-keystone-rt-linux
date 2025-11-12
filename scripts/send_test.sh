#!/usr/bin/expect -f

set timeout 60
set keystone_ip 192.168.1.160
set password sifive

spawn scp -o StrictHostKeyChecking=no -r /home/oscar/Cyberlab/Sources/PhD/Codes/keystone-for-real-time-system/keystone-6.6/build-hifive_unmatched64/buildroot.build/per-package/keystone-examples/target/usr/share/keystone/examples root@$keystone_ip:/usr/share/keystone
expect "password: "
send "$password\r"
expect eof