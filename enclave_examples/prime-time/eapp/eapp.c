#include <stdio.h>
#include <time.h>

int main()
{
  int max = 100000;
  printf("Staring prim with max: %d\n", max);
  clock_t t0 = clock();
  int p = prime(max);
  clock_t t1 = clock();
  double clock_diff = (t1 - t0) * 1000 / CLOCKS_PER_SEC;
  printf("Primes found: %d\n", p);
  printf("Calculation time: %f\n", clock_diff);
  return 0;
}


int prime(int max)
{
  int i, num = 1, primes = 0;

  while (num <= max) { 
      i = 2; 
      while (i <= num) { 
          if(num % i == 0)
              break;
          i++; 
      }
      if (i == num)
          primes++;

      num++;
  }

  return primes;
}