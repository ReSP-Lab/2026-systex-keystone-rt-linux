#!/usr/bin/expect -f

set timeout 600
set keystone_ip 192.168.1.189
set keystone_passwd sifive
set enclave_name [lindex $argv 0]
set enclave_arg [lindex $argv 1]

spawn ssh -o StrictHostKeyChecking=no root@$keystone_ip

expect "password:"
send "$keystone_passwd\r"

send "modprobe keystone-driver\r"
expect {
    "keystone enclave v1.0.0" {
        exp_continue
    }
    "# "
}


send "/usr/share/keystone/examples/$enclave_name.ke $enclave_arg\r"

expect "# "

send "logout\r"

expect "login: "

exit