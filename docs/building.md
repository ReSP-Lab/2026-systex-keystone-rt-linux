# Building 

The build process of keystone uses Buildroot. For fresh install, the initial build can be very long, depending on your internet connection, because it has to download all required packages, including the toolchain.

Prebuilt images for HiFive Unmatched are available `prebuilt-images/`, ready to be flashed on µSD card.

While Keystone originally supported both QEMU and HiFive Unmatched Rev. B platform, this work currently only supports HiFiuve Unmatched Rev. B.

<details>

> This is due to the version bump of Buildroot/Linux kernel which introduced a few incompatibilities in the builds. We fixed those necessary for HiFive Unmatched but were not able to totally fix QEMU. The build process succeeds but there is currently still a crash at boot when using QEMU.

</details>

## Requirement 

Keystone documentation recommends using Ubuntu 16.04/18.04/20.04 and derivatives. This artifact has been tested on Ubuntu 20.04.6.

To reduce the build time, it is recommended the most cores and RAM possible. We tested on a 16 cores / 64 GB system. Build time can take several hours, specially for first run.

The following dependencies (from keystone) are required to build the systems:

```bash
sudo apt update
sudo apt install autoconf automake autotools-dev bc \
bison build-essential curl expat jq libexpat1-dev flex gawk gcc git \
gperf libgmp-dev libmpc-dev libmpfr-dev libtool texinfo tmux \
patchutils zlib1g-dev wget bzip2 patch vim-common lbzip2 python3 \
pkg-config libglib2.0-dev libpixman-1-dev libssl-dev screen \
device-tree-compiler expect makeself unzip cpio rsync cmake ninja-build p7zip-full libncurses-dev
```

## Submodules

The modified version of Keystone is in the `keystone-rt/` submodule, which itself uses submodules for Buildroot.

You can simply initialise all of them using:

```bash
git submodule update --init --recursive --depth 1
```

> There may be an error when trying to clone the `keystone-for-realtime-linux/keystone-rt/overlays/keystone/board/cva6/cva6-sdk/buildroot` submodule, which can be safely ignored as it is not used for this work.

## Platform and variant selection


The platform is selected using the `KEYSTONE_PLATFORM` variable. When running from the root directory, it is set to `KEYSTONE_PLATFORM=hifive_unmatched` by default.

The system variant uses the `RT=y/n` flag (`RT=n` by default) to know whether to build the stock version (without the PREEMPT_RT patches) or the real-time one.

## Build

Current configurations correspond to the systems used for the article. If you want to modify them before building the systems, see [## Configurations](##Configurations).

Set the `RT=y/n` depending on which variant you want to build.

```bash
make RT=y
```

The sdcard.img will be located in the `keystone-rt/(...)/buildroot.build/images/sdcard.img`.

Once the image is ready, see [docs/preparing-the-boards.md](preparing-the-boards.md) to run it on a HiFive Unmatched board.


## Configurations

The Buildroot configuration can be edited using the following commands (change or remove the `RT` flag if necessary)

```bash
make RT=y buildroot-configure
```

The actual configs are located in [overlays/keystone/configs](keystone-rt/overlays/keystone/configs) under `riscv64_hifive_unmatched_defconfig` and `riscv64_hifive_unmatched_rt_defconfig`.

The corresponding Linux configuration can be edited with:

```bash
make RT=y linux-configure
```

The Linux config are located in [overlays/keystone/board/sifive/hifive-unmatched](keystone-rt/overlays/keystone/board/sifive/hifive-unmatched) under `linux-sifive-unmatched-defconfig` and `linux-sifive-unmatched-rt-defconfig`.

Depending on what you have changed, the target may need a global rebuild or not. See the [Buildroot manual](https://docs.keystone-enclave.org/en/latest/Getting-Started/QEMU-Compile-Sources.html) for more explanation.

## Advanced buildroot commands

To access all buildroot commands, you need to change the CWD to `cd keystone-rt` (or directly call the [keystone-rt/Makefile](keystone-rt/Makefile) using `make -C keystone-rt`). You need to manually set `KEYSTONE_PLATFORM=hifive_unmatched` and you can use the `BUILDROOT_TARGET=...` to call specific buildroot commands.

For more information on the available commands and arguments, see the [Keystone documentation](https://docs.keystone-enclave.org/en/latest/Getting-Started/QEMU-Compile-Sources.html) and [Buildroot manual](https://docs.keystone-enclave.org/en/latest/Getting-Started/QEMU-Compile-Sources.html)

