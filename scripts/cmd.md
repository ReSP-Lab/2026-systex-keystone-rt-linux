numactl --physcpubind=1 ./run-enclave-loop.sh 

stress-ng --all 1 --taskset 1,2,3 -t 10m -x netlink-task,swap --log-file stress-ng.log

cyclictest --affinity=1,2,3 -vm -i100 -p99 -t --duration=10m > cyclictest.log

ssh root@192.168.1.160

chrt 99 *cmd*