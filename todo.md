# TODO

## Attacks

- memory full
- disk I/O
- enclaves full
- Interrupt spam
- ...

Demo with measurable impact !

## Questions

- Time mode (S mode ? M mode ?)

## Additional features required for rt on keystone

- enclave interrupt controlled -> RT scheduler on SM (formally verified)
- garantie wall clock
  - Used the RDTIME pseudo-instruction to retrieve the relative wall-clock time from the system ? Precise enough ?
  - Still need to get absolute time from real world, how ? from the OS ? or a specific enclave for this ?
  
