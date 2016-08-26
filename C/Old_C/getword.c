#include<stdio.h>
#include<ctype.h>
#include<string.h>

#define MAXWORD 100
#define BUFSIZE 100//bufsiz is sepcial variate

char buf[BUFSIZE];
int bufp = 0;

int getch(void)
{
    return (bufp > 0 )? buf[--bufp] : getchar();
}
void ungetch(int c)
{
    if (bufp >= BUFSIZE)
        printf("ungetch: too many characters\n");
    else
        buf[bufp++] = c;
}

int getword(char *word, int lim) {
    char *w = word;//unknow
    int c;
    while (isspace(c = getch())) 
	    ;
    if (c != EOF) {
        *w++ = c;
    }
    // This point is reached
    if (!isalpha(c)) {
        *w = '\0';
        return c;
    }
    for ( ; --lim > 0; w++) {
        if (!isalnum(*w = getch())) {
            ungetch(*w);
            break;
        }
    }
    *w = '\0';
    return word[0];
}

main (){
    char word[MAXWORD];
    int wd;
	while ((wd = getword(word,MAXWORD)) != EOF) {
            putchar("\n",wd);
            printf(":%s:\n",word);
	}
        
}
