#include <stdio.h>
#include <limits.h>
#include <float.h>

int main()
{
    printf("char storage size: %lu\n", sizeof(char));
    printf("int storage size: %lu\n", sizeof(int));
    printf("unsigned int storage size: %lu\n", sizeof(unsigned int));
    printf("long storage size: %lu\n", sizeof(long));
    printf("short storage size: %lu\n", sizeof(short));

    printf("float max bytes: %lu\n", sizeof(float));
    printf("double max bytes: %lu\n", sizeof(double));
    printf("float max value: %E\n", FLT_MAX);
    printf("float min value: %E\n", FLT_MIN);
    printf("FLT: %d\n", FLT_DIG);
    return 0;
}
