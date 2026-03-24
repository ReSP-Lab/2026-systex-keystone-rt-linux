# [Artifact] Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V?

This is the artefact for our paper on **Keystone with Linux PREEMPT_RT: Real-Time Enclaves on RISC-V**, which we submitted at the SysTEX 26 workshop.

The aim of this work is to evaluate the impact of Keystone enclaves on a Linux system using the PREEMPT_RT patches. We mainly look at how quickly real-time tasks start up, both in mixed contexts (real-time tasks running alongside Keystone enclaves) and real-time enclaves (Keystone enclaves scheduled using real-time processes). The evaluation is done on a HiFive Unmatched Rev. B board.

This repo uses a changed version of Keystone as a submodule. The main differences from the main keystone branch are:

- Update the Buildroot version from 2023.02.2 to 2024.02.13 to support the Linux kernel 6.6.
- Update the Linux kernel version from 6.1.32 to 6.6.87. This will allow you to access the PREEMPT_RT patches for RISC-V.
- New build target variant, which will add the PREEMPT_RT patches and the related Linux kernel configurations.


## Usage

See the following docs

- [Building the image](docs/building.md)
    > The builds can take several hours. Therefore, prebuilt images for HiFive Unmatched Rev. B are available in `prebuilt-images/`.
- [Preparing the board](docs/preparing-the-boards.md)
- [Running the experiments](docs/running-the-experiments.md)
- [Making the figures](docs/making-figures.md)

## Citation

TODO
