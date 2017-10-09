#include<stdio.h>

#define LENGTH 10
#define WIDTH 5
#define NEWLINE '\n'

int main()
{
    int area;
    area = LENGTH * WIDTH;
    printf("value of area: %d", area);
    printf("%c", NEWLINE);

    const int length = 10;
    const int width = 5;
    const char newline = '\n';
    area = length * width;
    printf("value of area: %d", area);
    printf("%c", newline);
    return 0;
}
