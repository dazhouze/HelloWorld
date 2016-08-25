#include<stdio.h>

int main (void)
{
    int a[5] = {0};
    int b[5] = {[2] = 2, [3] = 3};
    int i;
    for (i = 0; i < 5; i++){
        printf("a element: %i\n", a[i]);
        printf("b element: %i\n", b[i]);
    } 
    printf("array size: %i\n", (int)(sizeof(a)/sizeof(a[0])));
}
