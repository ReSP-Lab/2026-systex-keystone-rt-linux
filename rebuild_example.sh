#! /bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cp -rf -R $SCRIPT_DIR/enclave_examples/. $SCRIPT_DIR/keystone/examples

cd $SCRIPT_DIR/keystone

BUILDROOT_TARGET=keystone-examples-dirclean make

make -j$(nproc)