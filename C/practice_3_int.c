#include<stdio.h>
int main (void)
{
    int i;
    float f;
    i = 899.9;
    f = 3.14159f;
    printf("i: %d, f: %f\n", i, f);
    i = i + f;
    printf("i: %d, f: %f\n", i, f);
    f = 1.0e2;
    f = 1.0E2;
    printf("i: %d, f: %f\n", i, f);
    printf("sizeof char:%lu int:%lu\n", sizeof(char), (long unsigned)sizeof(int));
    printf("size of int: %zu\n", sizeof(int));
    printf("size of double: %zu\n", sizeof(double));
}
