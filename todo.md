
## Attacks

- memory full
- disk I/O
- enclaves full
- ...

## Questions

- Wall clock sources ?
- One enclave running per core ?

## Additional features required for rt on keystone

- enclave interrupt controlled -> RT scheduler on SM (formally verified)
- garantie wall clock
  - Used the RDTIME pseudo-instruction to retrieve the wall-clock time from the system ? but how does it initialize ?