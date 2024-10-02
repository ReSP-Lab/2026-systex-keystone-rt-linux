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
  for (unsigned long i = 0; i < 100000000000; i++)
  {
    __asm__("nop");
  }
  end = read_cycles();
  total = end - start;
  printf("cycle=%lu\n", total);

  printf("Hold enclave end\n");
  return 0;
}