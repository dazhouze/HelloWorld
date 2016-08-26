#include<stdio.h>
#include<stdbool.h>    //only c99

bool prime (int n)
{
    if(n<1)
        return false;

    for (int i = 2; i < n; i++){
        if (n % i == 0){
            return false;
        }
    }
    return true;
}

int main (void)
{
    int num;
    printf("Please enter a number: ");

    if (!scanf("%d", &num))
        return -1;
    (void)printf("Set up the program.\n");

    if (prime(num))
        printf("%i is a prime number.\n", num);
    else
        printf("%i is not a prime number.\n", num);

    return 0;
}
