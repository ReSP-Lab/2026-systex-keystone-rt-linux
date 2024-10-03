- [1. Standard boot components](#1-standard-boot-components)
  - [1.1. \[ZSBL\] Zero Stage bootloader (M-mode) (ROM)](#11-zsbl-zero-stage-bootloader-m-mode-rom)
  - [\[FSBL\] First Stage Bootloader (M-mode) (DDR)](#fsbl-first-stage-bootloader-m-mode-ddr)
  - [1.2. \[RUNTIME\] Open Source Supervisor Binary Interface (M-mode)](#12-runtime-open-source-supervisor-binary-interface-m-mode)
  - [\[BOOTLOADER\] Last stage bootloader (S-mode)](#bootloader-last-stage-bootloader-s-mode)
- [2. Keystone SM (M-mode)](#2-keystone-sm-m-mode)
  - [2.1. Boot process](#21-boot-process)
    - [2.1.1. Cold-boot hart only](#211-cold-boot-hart-only)
      - [2.1.1.1. Register keystone custom extension](#2111-register-keystone-custom-extension)
      - [2.1.1.2. Initialize the SM memory region](#2112-initialize-the-sm-memory-region)
      - [2.1.1.3. Initialize the OS memory region](#2113-initialize-the-os-memory-region)
      - [2.1.1.4. Platform\_init\_global\_once](#2114-platform_init_global_once)
      - [2.1.1.5. Copy keypair from root of trust](#2115-copy-keypair-from-root-of-trust)
      - [2.1.1.6. Initialize the enclaves metadata](#2116-initialize-the-enclaves-metadata)
    - [2.1.2. memory barrier ?](#212-memory-barrier-)
    - [2.1.3. Initialize PMP](#213-initialize-pmp)
    - [2.1.4. Platform specific global init](#214-platform-specific-global-init)
    - [2.1.5. Print HASH](#215-print-hash)
- [3. Enclave lifecycle](#3-enclave-lifecycle)
  - [3.1. Enclave initialization](#31-enclave-initialization)
    - [3.1.1. Host app](#311-host-app)
  - [3.2. Enclave ocall](#32-enclave-ocall)
  - [3.3. Enclave run](#33-enclave-run)
  - [3.4. Enclave stop](#34-enclave-stop)
    - [3.4.1. Ocall](#341-ocall)
    - [3.4.2. interruption](#342-interruption)
  - [3.5. Enclave resume](#35-enclave-resume)
  - [3.6. Enclave exit](#36-enclave-exit)
  - [3.7. Enclave destruction](#37-enclave-destruction)



Starting point -> [sm.c](src/sm.c)

ecall_handler for keystone sm -> [sm-sbi-opensbi](src/sm-sbi-opensbi.c)

Trap is added in [trap.S](src/trap.S) and link into [sbi_trap_hack.c](src/sbi_trap_hack.c) to handle interrupt for **IRQ_M_TIMER** and **IRQ_M_SOFT** `mcause`

# 1. Standard boot components

CPU reset jump to `0x10000000`

## 1.1. [ZSBL] Zero Stage bootloader (M-mode) (ROM)
> Then jump to the hardcoded address `0x80000000`

## [FSBL] First Stage Bootloader (M-mode) (DDR)

Example: U-Boot SPL, Coreboot

> Initialize some register

- `a0`: hard id
- `a1`: pointer to the device tree data struct
- `a2`: Pointeur to the `struct fw_dynamic_info` to tell the runtime (OpenSBI) how to acces the bootloader
  
## 1.2. [RUNTIME] Open Source Supervisor Binary Interface (M-mode)
> BIOS
> Responsible of hardware initialization, boot OS in S-mode (second stage bootloader) and provide interrupt-based OS services to interface the platform specific firmware.

> There is 3 possible options related to the loading of the next stage: 
- `FW_PAYLOAD`
  > Put the next stage just next to OpenSBI (need to be linked during OpenSBI compilation).
- `FW_JUMP`
  > Hardcode the address of the next stage and OpenSBI jump to it at the end (still need to be set during compilation but more flexible)
- `FW_DYNAMIC`
  > Previous stage is responsible for setting up the next stage pointer to a `struct fw_dynamic_info` in register `a2`, which will be used by OpenSBI to boot the next stage.

> `FW_DYNAMIC` is generally used since it offer the most flexibility.

## [BOOTLOADER] Last stage bootloader (S-mode)

Example: U-Boot

> Responsible for loading the OS

# 2. Keystone SM (M-mode)

> This is a modifier version of OpenSBI with a custom extension (Keystone's EID is `0x08424b45`)

more info in [spec v1.0](spec/v1.0.md)

## 2.1. Boot process

### 2.1.1. Cold-boot hart only

#### 2.1.1.1. Register keystone custom extension


Register the custom extension to OpenSBI, with the extension id = `0x08424b45` and link to the keystone sbi_ecall handler.

> This is only executed by the cold_boot hart

#### 2.1.1.2. Initialize the SM memory region

start_addr = `0x80000000`
size = `0x200000`
priority = `PMP_PRI_TOP`
region_id = `-1`
overlap = `false`

#### 2.1.1.3. Initialize the OS memory region

start_addr = `0x00000000`
size = `-1`
priority = `PMP_PRI_BOTTOM`
region_id = `-1`
overlap = `false`

-> napot_region_init

#### 2.1.1.4. Platform_init_global_once

#### 2.1.1.5. Copy keypair from root of trust

This copy the key from the system root of trust (for generic, it copy it from sanctum bootroom, manually initialize pointer, but dk where do the values come)

```
sm_hash
sm_signature
sm_secret_key
m_public_key
dev_public_key
```

#### 2.1.1.6. Initialize the enclaves metadata

For all possible enclave, set the state to INVALID and clear the region, them call the platform specific init for the enclave.


### 2.1.2. memory barrier ?

`mb` once at the cold-boot init end for each hart

TODO more

### 2.1.3. Initialize PMP

It initialize the PMP regions

TODO more

Set the PMP for SM (with no perm)
Set the PMP for OS (with all perm)

### 2.1.4. Platform specific global init

...

### 2.1.5. Print HASH

Print the sm_hash

# 3. Enclave lifecycle

## 3.1. Enclave initialization

### 3.1.1. Host app

SM call: `SBI_SM_CREATE_ENCLAVE`

with arg:

```
uintptr_t eid;

// host -> driver
uintptr_t min_pages; // create
uintptr_t utm_size; // utm_init

// host -> driver // finalize
uintptr_t runtime_paddr;
uintptr_t user_paddr;
uintptr_t free_paddr;
uintptr_t free_requested;

// driver -> host
uintptr_t epm_paddr;
uintptr_t epm_size;
uintptr_t utm_paddr;
```




## 3.2. Enclave ocall

## 3.3. Enclave run

```
uintptr_t eid;
uintptr_t error;
uintptr_t value;
```

## 3.4. Enclave stop

### 3.4.1. Ocall

### 3.4.2. interruption

## 3.5. Enclave resume

## 3.6. Enclave exit

## 3.7. Enclave destruction