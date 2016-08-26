#include<stdio.h>
#define IN  1
#define OUT 0

main(){
    int state , c ;
    state = OUT;
    while ((c=getchar()) != EOF){
        if (c == '\t'){
            if (state == IN){
                state = OUT;
                putchar(' ');
                putchar(' ');
                putchar(' ');
                putchar(' ');
            }else {
                state = IN;
                putchar(' ');
                putchar(' ');
                putchar(' ');
                putchar(' ');
            }
        }else if(state == OUT) {
            putchar(c);
        }else {
            putchar(' ');
        }
    }
}
