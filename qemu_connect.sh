#! /bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

sudo ssh-keygen -f "/root/.ssh/known_hosts" -R "[localhost]:9821"
clear
sudo ssh -o StrictHostKeyChecking=accept-new -p 9821 root@localhost