#include <stdio.h>

int main() 
{
    int a = 5;
    //prefix
    printf("value = %d\n", a);
    printf("prefix = %d\n", ++a);
    printf("current = %d\n", a);

    printf("prefix = %d\n", --a);
    printf("current = %d\n", a);

    //postfix
    printf("value = %d\n", a);
    printf("postfix = %d\n", a++);
    printf("currnet = %d\n\n", a);

    printf("postfix = %d\n", a--);
    printf("currnet = %d\n", a);

    return 0;
}