#include<stdio.h>
#include<string.h>

int count_space(char s[]);

int main (void)
{
    char ss[] = "abc";
    (void)count_space(ss);
    printf("ss: %s\n", ss);
    strcpy(ss, "efg");
    printf("ss: %s\n", ss);
}

int count_space(char str[]){
    str[1] = 'd';
    return 0;
}
