#!/bin/bash

export KEYSTONE_PLATFORM=hifive_unmatched
#export RT=y

make -C keystone-6.6/ BUILDROOT_TARGET=keystone-examples-dirclean
make -C keystone-6.6/ BUILDROOT_TARGET=keystone-examples-install
