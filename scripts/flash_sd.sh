#!/usr/bin/bash

set -e

SD_DEV=mmcblk0
TYPE=_rt


if lsblk | grep -q "$SD_DEV"; then
    echo "flashing device..."
    sudo dd if=keystone-6.6/build-hifive_unmatched64$TYPE/buildroot.build/images/sdcard.img of=/dev/$SD_DEV bs=1M status=progress
else
    echo "Device $SD_DEV is not connected."
fi


    