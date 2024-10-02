//******************************************************************************
// Copyright (c) 2018, The Regents of the University of California (Regents).
// All Rights Reserved. See LICENSE for license details.
//------------------------------------------------------------------------------
#include "eapp_utils.h"
#include "string.h"
#include "edge_call.h"
#include <syscall.h>
#include <stdio.h>

#define OCALL_SLEEP 1
#define OCALL_PRINT 2

unsigned long ocall_sleep();
unsigned long ocall_print(unsigned long nb_cycle);

unsigned long read_cycles(void)
{
  unsigned long cycles;
  asm volatile ("rdcycle %0" : "=r" (cycles));
  return cycles;
}

int main(){
  unsigned long arg = 34;
  unsigned long nb_cycle;
  for (int i = 0; i < 20; i++){
    unsigned long start = read_cycles();
    ocall_sleep();
    unsigned long end = read_cycles();
    nb_cycle = end - start;
    ocall_print(nb_cycle);
  }

  EAPP_RETURN(0);
}

unsigned long ocall_sleep(){
  unsigned long retval;
  ocall(OCALL_SLEEP, NULL, 0, &retval, sizeof(unsigned long));
}

unsigned long ocall_print(unsigned long nb_cycle){
  unsigned long retval;
  ocall(OCALL_PRINT, &nb_cycle, sizeof(unsigned long), &retval, sizeof(unsigned long));
}
