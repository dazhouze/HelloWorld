#include<stdio.h>

#define MAXHIST 15
#define MAXWORD 11
#define IN  1
#define OUT 0

main(){
    int c , ndigit[12] , i , len , state;
    len = 0;
    state = OUT;

    for (i = 0; i <= MAXWORD; ++i)
        ndigit[i]=0;

    while ((c=getchar()) != EOF){
        if (c == '\n' || c == '\t' || c == ' '){
            state = OUT;
            if (len <= MAXWORD)
                ++ndigit[len];
            len = 0;
        }else if (state == OUT){
            state = IN;
            len=1;
        }else
            ++len;
    }
/*1234567*/
    int maxValue;
    maxValue = 0;
    printf ("digits=\n");
    for (i=1 ; i <= MAXWORD ; ++i){
        printf(" %d",ndigit[i]);
        if (ndigit[i] > maxValue)
            maxValue = ndigit[i];
    }
    printf ("\n");
    for (i=1 ; i <= MAXWORD ; ++i){
        printf("%d\t",i);
        int max , bar;
        if (ndigit[i] >= MAXHIST)
            max = MAXHIST;
        else
            max = ndigit[i];
        if (max == 0)
            printf("0");
        for (bar=1 ; bar<=max ; ++bar){
            printf("*");
        }
        printf("\n");
    }
    printf ("\n");
    
    int j;
    for (i=MAXHIST ; i >= 1 ; --i){
        for (j=1; j <= MAXWORD ; ++j){
            int max , bar;
            if (ndigit[j] >= i)
                printf("\t*");
            else 
                printf("\t ");
        }
        printf("\n");
    }
    for (j=1; j <= MAXWORD ; ++j){
        printf ("\t%d", j);
    }
    printf("\n");
}
