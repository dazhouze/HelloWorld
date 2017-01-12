#include<stdio.h>
#include"max.h"
//#include"max.c"
//int max();
int main (int argv, char* argc[]) 
{
    printf("Hello world.\n");
    int a = 35;
    int b = 32;
    printf("the max is:%d\n", max(a, b));
    fprintf(stderr, "the max is:%d\n", max(a, b));
    return 0;
}
