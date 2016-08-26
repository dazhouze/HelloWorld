#include <stdio.h>
#define MAXLINE 1000

main(int argc, char *argv[])
{
    char line[MAXLINE];
    FILE *fp;
    if ((fp = fopen( *++argv, "rb")) != NULL)
        while (fgets(line, MAXLINE, fp) != NULL)
            printf("%d", line);

    return 0;
}

char *split(char *part, int n, char *whole, int separator)
{
    
}
