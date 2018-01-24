#include <stdio.h>
extern int count;
void write_extern(void)
{
    printf("count is %2d\n", count);
}
