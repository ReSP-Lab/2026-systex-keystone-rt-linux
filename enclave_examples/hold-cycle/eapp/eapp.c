#include <stdio.h>

unsigned long read_cycles(void)
{
  unsigned long cycles;
  asm volatile ("rdcycle %0" : "=r" (cycles));
  return cycles;
}

int main()
{
  printf("Staring hold enclave\n");
  unsigned long start, end, total;

  start = read_cycles();
  end = start;
  while (end-start < 10000000000){
    end = read_cycles();
  }
  total = end - start;
  printf("cycle=%lu\n", total);

  printf("Hold enclave end\n");
  return 0;
}