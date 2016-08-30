#include<stdio.h>
#include<stdlib.h>

#define N 10

void quickSort();
int split();

int main (void)
{
    printf("Enter 10 num to be sorted: ");
    int a[N], i;
    for (i = 0; i < N; i++) 
        if (!scanf("%d", &a[i]))
            exit(-1);
    quickSort(a, 0, N - 1);
    printf("In sorted order: ");
    for (i = 0; i < N; i++)
        printf("%d ", a[i]);
    printf("\n");

    return 0;
}

void quickSort(int a[], int low, int high)
{
    int middle;

    if (low >= high) 
        return;
    middle = split(a, low, high);
    quickSort(a, low, middle - 1);
    quickSort(a, middle + 1, high);
}

int split(int a[], int low, int high)
{
    int part_element = a[low];

    for (;;) {
        while (low < high && part_element <= a[high])
            high--;
        if (low >= high) 
            break;
        a[low++] = a[high];

        while (low< high && a[low] <= part_element)
            low++;
        if (low >= high)
            break;
        a[high--] = a[low];
    }

    a[high] = part_element;
    return high;
}
