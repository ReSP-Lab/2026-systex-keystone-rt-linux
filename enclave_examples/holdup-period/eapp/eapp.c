//******************************************************************************
// Copyright (c) 2018, The Regents of the University of California (Regents).
// All Rights Reserved. See LICENSE for license details.
//------------------------------------------------------------------------------
#include "eapp_utils.h"
#include "string.h"
#include "edge_call.h"
#include <syscall.h>

#define OCALL_PRINT_STRING 1

unsigned long ocall_print_string(char* string);

int main(){

  ocall_print_string("Starting native prime");
  for (int i = 0; i < 100; i++)
  {
    for (int i=0; i<1000000000; i++){
      __asm__("nop");
    }
    ocall_print_string("...");
  }

  ocall_print_string("Ending native prime");

  EAPP_RETURN(0);
}

unsigned long ocall_print_string(char* string){
  unsigned long retval;
  ocall(OCALL_PRINT_STRING, string, strlen(string)+1, &retval ,sizeof(unsigned long));
  return retval;
}

