#include <stdio.h>
#include <math.h>

int main(){
    FILE *fp;
    char ch; 
    fp=fopen("./HelloWorld.txt","r");
    ch=fgetc(fp);
    while(ch!=EOF) 
    { 
        putchar(ch); 
        ch=fgetc(fp); 
    } 
    fclose(fp); 
}
