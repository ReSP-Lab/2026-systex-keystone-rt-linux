# [Artifact] Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V?

This is the artifact for our **Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V?** paper submitted at the SysTEX"26 workshop.

This work aims at evaluating the impact of Keystone enclaves on a Linux system using the PREEMPT_RT patches. In particular, we focus on startup latencies of real-time tasks, both for mixted context (real-time task running along side Keystone enclave) and real-time enclave (Keystone enclave scheduled using real-time processes). The evaluation are done on a HiFive Unmatched Rev. B board.

This repo use a modified version of Keystone as a submodule. The main differences from the main keystone branch are:

- Updated Linux kernel version (from 6.1.32 to 6.6.87) to have acces to the PREEMPT_RT patches for RISC-V (available as standalone).
- New build target for RT variant which add the PREEMPT_RT patches and related Linux kernel configurations.

## Installation

Clone this repo then initialize the submodules:

```bash
git submodule update --init --recursive --depth 1
```

> There may be an error when trying to clone the `keystone-for-realtime-linux/keystone-rt/overlays/keystone/board/cva6/cva6-sdk/buildroot` submodule, which can be safely ignore as it is not used for this work

## Usage

See the following docs

- [Building the image](docs/building.md)
    > Prebuilt image for HiFive Unmatched Rev. B are available in TODO since the build process can be very long.
- [Preparing the board](docs/preparing-the-boards.md)
- [Running the experiments](docs/running-the-experiments.md)
- [Making the figures](docs/making-figures.md)

## Citation

TODO
