# Building 

## Requirement 

Keystone documentation recommand using Ubuntu 16.04/18.04/20.04 and derivative. This artifact has been tested using Ubuntu 20.04.6.

If you are using newer system, make sure to configure GCC to use GCC 14 when building keystone or you may encounter compilation errors during buildroot configuration.

The following dependencies are required to build the systems using buildroot

```bash
sudo apt update
sudo apt install autoconf automake autotools-dev bc \
bison build-essential curl expat jq libexpat1-dev flex gawk gcc git \
gperf libgmp-dev libmpc-dev libmpfr-dev libtool texinfo tmux \
patchutils zlib1g-dev wget bzip2 patch vim-common lbzip2 python3 \
pkg-config libglib2.0-dev libpixman-1-dev libssl-dev screen \
device-tree-compiler expect makeself unzip cpio rsync cmake ninja-build p7zip-full libncurses-dev
```

## Configurations

The buildroot configs are located in [overlays/keystone/configs](keystone-rt/overlays/keystone/configs) under `riscv64_hifive_unmatched_defconfig` and `riscv64_hifive_unmatched_rt_defconfig`.


They can be edited using the following commands

```bash
make KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt buildroot-configure
```

and

```bash
make RT=y KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt buildroot-configure
```

The respective linux config are located in [overlays/keystone/board/sifive/hifive-unmatched](keystone-rt/overlays/keystone/board/sifive/hifive-unmatched) under `linux-sifive-unmatched-defconfig` and `linux-sifive-unmatched-rt-defconfig`.

They can be edited using the following commands

```bash
make KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt linux-configure
```

and

```bash
make RT=y KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt linux-configure
```

For more information on the available commands and arguments, see the [keystone documentation](https://docs.keystone-enclave.org/en/latest/Getting-Started/QEMU-Compile-Sources.html)


## Build

To build the system without PREEMPT_RT

```bash
make KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt
```
To build the system with PREEMPT_RT

```bash
make RT=y KEYSTONE_PLATFORM=hifive_unmatched -C keystone-rt
```

The sdcard.img will be located in the `keystone-rt/(...)/buildroot.build/images/`