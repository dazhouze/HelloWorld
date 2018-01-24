#include<stdio.h>

void func1(void);

static int count=10;

int main()
{
    while(count--){
        func1();
    }
}

void func1(void)
{
    static int thingy = 5;
    thingy++;
    count--;
    printf("thingy is %2d, count is %2d\n", thingy, count);    
}
