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

unsigned long ocall_sleep();

unsigned long read_cycles(void)
{
  unsigned long cycles;
  asm volatile ("rdcycle %0" : "=r" (cycles));
  return cycles;
}

unsigned long fibonacci_rec(unsigned long in){
  if( in <= 1)
    return 1;
  else
    return fibonacci_rec(in-1)+fibonacci_rec(in-2);
}

// Returns the number of cycles for a given fibonacci execution
unsigned long fib_eapp(unsigned long in) {
  unsigned long start = read_cycles();
  fibonacci_rec(in);
  unsigned long end = read_cycles();
  return end - start;
}

int main(){
  unsigned long arg = 34;
  unsigned long nb_cycle;
  for (int i = 0; i < 20; i++){
    nb_cycle = fib_eapp(arg);
    ocall_sleep(&nb_cycle);
  }

  EAPP_RETURN(0);
}

unsigned long ocall_sleep(unsigned long* nb_cycle){
  unsigned long retval;
  ocall(OCALL_SLEEP, nb_cycle, sizeof(unsigned long), &retval, sizeof(unsigned long));
}
