#include<stdio.h>

int main (int argv, char* argc[]) 
{
    printf("Hello world.\n");
    printf("argv:%d\n", argv);
    for (int i=0; i<argv; i++){
        printf("argc[%d]:%s\n", i, argc[i]);
    }
    return 0;
}
