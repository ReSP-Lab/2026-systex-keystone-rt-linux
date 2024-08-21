- [1. Necessary Dependencies and keystone repo setup](#1-necessary-dependencies-and-keystone-repo-setup)
- [2. Compile Sources](#2-compile-sources)
  - [2.1. Build All Components](#21-build-all-components)
  - [2.2. Rebuilding Changed Components](#22-rebuilding-changed-components)
  - [2.3. Appendix A: Configuring Buildroot and the Linux Kernel](#23-appendix-a-configuring-buildroot-and-the-linux-kernel)
  - [2.4. Appendix B: Debugging Failed Builds](#24-appendix-b-debugging-failed-builds)
- [3. Running and Testing Keystone on QEMU](#3-running-and-testing-keystone-on-qemu)
  - [3.1. Launching Keystone in QEMU](#31-launching-keystone-in-qemu)
  - [3.2. Debugging Keystone in QEMU](#32-debugging-keystone-in-qemu)


>This is the QEMU demo documentation from the [keystone docs](http://docs.keystone-enclave.org/en/latest/Getting-Started/Running-Keystone-with-QEMU.html)

# 1. Necessary Dependencies and keystone repo setup

The first two step of the demo are installing the dependencies and setting up the keystone repo. The `setup.sh` script can be used to do this directly.

```sudo ./setup.sh```


# 2. Compile Sources

## 2.1. Build All Components

We use Make and Buildroot as a build system. The top-level Makefile is located in the root directory of the repository and is the main frontend to the build system. It collects configuration options and initiates the build process, which itself takes place in Buildroot.

Use the following command to initiate a build of all components:

```make -j$(nproc)```

This will build all Keystone components and generate a bootable image for QEMU, placing the build output in `build-$PLATFORM$BITS`.

A build can be configured with the following options (along with their default values). The values must be passed to the build as environment variables, either through an export in the shell, or by passing them directly to `make` by prepending them to the command (e.g. `OPTION1=VALUE1 OPTION2=VALUE2 (...) make`):

- `KEYSTONE_PLATFORM=generic`: Configures the platform to build for. Currently, only the `generic` QEMU virtual platform is supported.

- `KEYSTONE_BITS=64`: Configures if the build is for RV64 or RV32.

- `BUILDROOT_CONFIGFILE=qemu_riscv$(KEYSTONE_BITS)_virt_defconfig`: Configures the buildroot config file to use.

- `BUILDROOT_TARGET=all`: Configures the target to be built. (e.g. `keystone-sm`, for the security monitor)


## 2.2. Rebuilding Changed Components

In a very common workflow, a developer would make changes to a component and then rebuild the component. As built packages are synced to various other places by Buildroot, this can be prone to stale and thus incorrect builds.

To avoid this, changes to components are detected by using content-adressed versioning of the component sources, allowing Buildroot to detect builds that include stale sources. In such cases, a warning is printed when executing the build.

A stale source is then removed by using the following command:

```BUILDROOT_TARGET=<target>-dirclean make -j$(nproc)```

This will remove the stale source directory. Afterwards, a new build can be initiated as usual.

## 2.3. Appendix A: Configuring Buildroot and the Linux Kernel

There are convenience targets in the top-level Makefile to configure both Buildroot and the Linux kernel.

To configure Buildroot, use the following command:

`make buildroot-configure`

To configure the Linux kernel, use the following command:

`make linux-configure`

These commands open a menu-based configuration interface. After making changes, save the configuration and exit the interface. The Makefile takes care of placing the configuration files in the correct locations.

## 2.4. Appendix B: Debugging Failed Builds

As the Buildroot output is very verbose, only certain parts of it are printed to `stdout` by default. The full output of a build is written to `build-$PLATFORM$BITS/build.log`, which can be used to debug failed builds.


# 3. Running and Testing Keystone on QEMU

## 3.1. Launching Keystone in QEMU

The following command will run QEMU, starting execution from the emulated silicon root of trust. The root of trust then jumps to the SM, and the SM boots Linux!

```make run```

Login as `root` with the password `sifive`.

You can exit QEMU by `ctrl-a``+``x` or using poweroff command

>Note
>
>Note that the launch scripts for QEMU will start ssh on a forwarded localhost port. The script will print what port it has forwarded ssh to on start.

Start the Keystone driver by running the following command in the QEMU guest:

```modprobe keystone-driver```

Then find the included files (i.e. enclave applications) in `/usr/share/keystone/examples`. To launch an enclave application, just execute it:

```/usr/share/keystone/examples/hello.ke```

## 3.2. Debugging Keystone in QEMU


> Error ?
>
> Change in gdb/generic line 10 : `{builddir}/linux-6.1.32/vmlinux-gdb.py -> {builddir}/linux-6.1.32/scripts/gdb/vmlinux-gdb.py` ???

To debug a Keystone build with GDB, run the following command to start QEMU in debug mode:

```KEYSTONE_DEBUG=y make run```

Then, in another terminal, run the following command to connect to the GDB server:

```make debug-connect```

This will connect to the GDB server running in QEMU. You can then use GDB as normal to debug the Keystone build. In addition to the normal GDB commands, the following Keystone-specific commands are available after running `source scripts/gdb/pmp.py` (in GDB):

- `pmp-clear`: Clear the PMP CSRs

- `pmp-dump`: Show the current state of the PMP CSRs

To resume the QEMU instance, you need to pass `continue` to the GDB server.




