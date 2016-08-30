#include<stdio.h>
#include<stdbool.h>
#include<stdlib.h>

#define STACK_SIZE 100

/* external varibales
 * also known as globle varibles
 * functional area is the whole file
 */
int contents[STACK_SIZE]; //stack
int top = 0; //position of stack top

void make_empty(void)
{
    top = 0;
}

bool is_empty(void){
    return top == 0;
}


bool is_full(void){
    return top == STACK_SIZE;
}

void push(int i)
{
    if(is_full())
        stack_overflow();
    else
        contents[top++] = i;
}

int pop(void){
    if (is_empty())
        stack_underflow();
    else
        return contents[--top];
}

int main (void)
{

    return 0;
}
