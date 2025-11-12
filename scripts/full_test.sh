#!/usr/bin/bash

set -eu

exec > >(tee -a full.log) 2>&1

./rebuild_test.sh

./send_test.sh

./run_test_latency.sh