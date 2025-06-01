#include <stdio.h>

int main() 
{
    int total = 10000;
    printf("before = %d\n", total);
    int x = 3;
    total *= x;
    printf("total = %d\n", total);
    int mouse_price = 500;
    total += mouse_price;
    printf("total = %d\n", total);
    return 0;
}