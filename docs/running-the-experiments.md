# Running the experiments

Since the experiment are running stressors (stress-ng and iper3f) set to use all system ressources, the system will most likely become unresponsible for the duration of the experiment. You can use the `--skip-load` or `-s` flag to start a test run without theses stressors.

## Iperf3

Since we are using iperf3 (server) to simulate network interupt, we need to start a client from a remote machine on the same network and point it to the server.

You can install iperf3 using `sudo apt install iperf3`.

When starting the experiment, the script will ask you to start the iperf3 client. You can run it with the following commands (set the correct ip address and adjust the `-t 5800` to a duration higher than the experiment)

```bash
iperf3 -c 192.168.1.X -p 5201 -w 64k -P 100 -t 5800
```

## Experiment 1

This experiment measure the startup scheduling latencies of high-priority Linux process during high load. Cyclictest is used to measure the latencies while iperf3 and stress-ng put pressurs on the system.

The following command can be used to run this experiment:

```bash
./run-linux-cyclictest.sh --duration 60m
```

If the stressors are not skip (using `--skip-load`), it will as to start the iperf3 client (see [## Iperf3](##Iperf3)).

The latencies are recorded in the `cyclictest.log` file, starting directly after the start of the stressors. During the compilation of the graph, the first X sample can be remove to exclu the imapct of a transission periode.

## Experiment 2

This experiment is basically the same as the previous one, but with the introduction of Keystone enclave in the background.

The following command can be used to run this experiment:

```bash
./run-linux-cyclictest.sh --duration 60m --enclave-loop
```

If the stressors are not skip (using `--skip-load`), it will as to start the iperf3 client (see [## Iperf3](##Iperf3)).

The latencies are recorded in the `cyclictest.log` file, starting directly after the start of the stressors. During the compilation of the graph, the first X sample can be remove to exclu the imapct of a transission periode.

### Experiment 3

This experiment measure the startup scheduling latencies of keystone enclave spawn from high priority process. A modified version of cyclictest is used insided an enclave to measure the latencies while iperf3 and stress-ng put pressurs on the system.

The following command can be used to run this experiment:

```bash
./run-enclave-cyclictest.sh --duration 10m --threads 2 --loops 60 --delay 30 --cpus 0-1
```

You can adjust the number of threads and iteration for each, as well as the initial delay to ensure the system is under load when we start the measurement.

If the stressors are not skip (using `--skip-load`), it will as to start the iperf3 client (see [## Iperf3](##Iperf3)).

> Due to an issue from Keystone, creating more than ~150 enclaves from a process will likely result in core halt. To get more measurement, you can simply save the `cyclictest.log` file then re-run the same experiment and combine the measurements.

> Due to an issu from the HiFive Unmatched board, where some core's PMP seems to have an hardware wearout. You may want to fix the exact cores used with `--cpu`.

The latencies are recorded in the `cyclictest.log` file.

see [docs/making-figures.md](docs/making-figures.md) to generate the graph.