#! /bin/bash

echo "Setting up dependencies"

sudo apt update
sudo apt install autoconf automake autotools-dev bc bison build-essential curl expat jq libexpat1-dev flex gawk gcc git gperf libgmp-dev libmpc-dev libmpfr-dev libtool texinfo tmux patchutils zlib1g-dev wget bzip2 patch vim-common lbzip2 python3 pkg-config libglib2.0-dev libpixman-1-dev libssl-dev screen device-tree-compiler expect makeself unzip cpio rsync cmake ninja-build p7zip-full -y

echo "Setting up keystone"

git clone --recurse-submodules https://github.com/keystone-enclave/keystone.git

