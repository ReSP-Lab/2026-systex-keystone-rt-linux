#include <stdio.h>

int main()
{
  printf("Staring holdup enclave\n");
  while (0==0){
    __asm__("nop");
  }
  printf("Ending holdup enclave\n");
  return 0;
}