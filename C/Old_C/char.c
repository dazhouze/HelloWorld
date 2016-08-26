#include <stdio.h>

int main(){
    double d = 3.1415926;
    char ch = *(char*)&d;
    printf("%s\n", d);
    int i = 37;
    float f = *(float*)&i;
    printf("%d\n", f);
}
