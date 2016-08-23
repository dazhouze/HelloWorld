/*Adds two fractions*/

#include<stdio.h>
int main (void)
{
    int num1, denom1, num2, denom2, res_num, res_denom;
    printf("Enter first franction:");
    scanf("%d/%d", &num1, &denom1);

    printf("Enter first franction:");
    scanf("%d/%d", &num2, &denom2);
    
    res_num = num1 * denom2 + num2 * denom1;
    res_denom = denom1 * denom2;
    printf("The sum id %d/%d\n", res_num, res_denom);
}
