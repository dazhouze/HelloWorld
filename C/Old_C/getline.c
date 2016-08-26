#include <stdio.h>
#include <string.h>
#include "calc.h"

#define MAXLINE 1000
//int getline(char *s, int lim);

//char* month_name(int n);

int getline(char *s, int lim)//lim is max line number
{
    int c,i;
    for (i=0; (c=getchar())!=EOF && c!='\t' && c!='\n'; ++i)
        *s++ = c;
    if (c == '\n') {
        *s++=c;
        ++i;
    }
    *s++='\n';
    return i;
}

/*
char* month_name(int n)
{
    static char *name[] = {
        "Illegal month",
        "January","Febrary"
    };
    return name[n];
}
*/
