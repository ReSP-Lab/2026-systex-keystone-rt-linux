# Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V?

This is the artifact for our **Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V?** paper submitted at the SysTEX"26 workshop.

This work aim at evaluating the impact of Keystone on a Linux system using the PREEMPT_RT patches. In particular, we focus on startup latencies of real-time tasks, both for mixted context (real-time task running along side Keystone enclave) and real-time enclave (Keystone enclave scheduled using real-time processes). The evaluation are done on a HiFive Unmatched Rev. B board.

This repo use a modified version of Keystone as a submodule. The main differences from the main keystone branch are:

- Updated Linux kernel version (from 6.1.32 to 6.6.87) to have acces to the PREEMPT_RT patches for RISC-V (available as standalone).
- New build target for RT variant which add the PREEMPT_RT patches and related Linux kernel configurations.

## Installation

Clone this repo then initialize the submodules:

```bash
git submodule update --init --recursive --depth 1
```

> There may be an error when trying to clone the `keystone-for-realtime-linux/keystone-rt/overlays/keystone/board/cva6/cva6-sdk/buildroot` submodule, which can be safely ignore as it is not used for this work

Keystone use Buildroot to build the systems. Since the build time can be quite significant (specially for fresh build), we provide ready to use image for the HiFive Unmatched board. This does method only require to have `git` and `dd` (or another tool to flash sd card).


If you want to build the image yourself to make some change, you will have some requirement for yourt system. Please refer to [docs/building.md.md](docs/building.md) in that case.

## Flashing the image

If you are using the provided ready-to-use image, you can find them under TODO. You can flash them into an µSD card using the following command.

```bash
sudo dd if=images/hifive_unmatched64.img of=/path/to/sd/card bs=1M status=progress
```

To flash the version with the PREEMPT_RT patch, change the file to `images/hifive_unmtached64_rt.img` instead.


## Connection to the boards

Once the sd card in plugged in and the HiFive Unmatched board is powered up, you can either connect to it using SSH or via the serial connection of the board (we recommand using `minicom`). The root password is `hifive`.

## Experiments

To run the same experiment as in our article, see [docs/running-the-experiments.md](docs/running-the-experiments.md)

## License


