#include <stdio.h>

int main() 
{
    int num1, num2;

    printf("number1 = ");
    scanf("%d", &num1);
    printf("number2 = ");
    scanf("%d", &num2);

    printf("-----------------------\n");
    printf("%d + %d = %d\n", num1, num2, num1+num2);
    printf("%d - %d = %d\n", num1, num2, num1-num2);
    printf("%d x %d = %d\n", num1, num2, num1*num2);
    printf("%d / %d = %d\n", num1, num2, num1/num2);
    printf("%d mod %d = %d\n", num1, num2, num1%num2);
    return 0;
}