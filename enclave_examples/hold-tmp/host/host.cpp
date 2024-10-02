//******************************************************************************
// Copyright (c) 2018, The Regents of the University of California (Regents).
// All Rights Reserved. See LICENSE for license details.
//------------------------------------------------------------------------------
#include "edge/edge_call.h"
#include "host/keystone.h"

using namespace Keystone;

int
main(int argc, char** argv) {
  Enclave enclave;
  Params params;
  unsigned long cycles1, cycles2, cycles3, cycles4;

  params.setFreeMemSize(48* 1024 * 1024);
  params.setUntrustedSize(2 * 1024 * 1024);

  asm volatile("rdcycle %0" : "=r"(cycles1));

  enclave.init(argv[1], argv[2], argv[3], params);
  asm volatile("rdcycle %0" : "=r"(cycles2));
  printf("[keystone-hold-tmp] Init: %lu cycles\r\n", cycles2 - cycles1);

  enclave.registerOcallDispatch(incoming_call_dispatch);
  edge_call_init_internals(
      (uintptr_t)enclave.getSharedBuffer(), enclave.getSharedBufferSize());

  asm volatile("rdcycle %0" : "=r"(cycles3));
  enclave.run();
  asm volatile("rdcycle %0" : "=r"(cycles4));
  printf("[keystone-hold-tmp] Runtime: %lu cycles\r\n", cycles4 - cycles3);

  return 0;
}