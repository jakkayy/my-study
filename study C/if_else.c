#include <stdio.h>

int main() 
{
    int num1, num2;
    printf("Input num1 = ");
    scanf("%d", &num1);
    printf("Input num2 = ");
    scanf("%d", &num2);

    if (num1 < num2) {
        printf("%d < %d\n", num1, num2);
    } else if (num1 == num2) {
        printf("%d = %d\n", num1, num2);
    } else {
        printf("%d < %d\n", num1, num2); 
    }
    return 0;
}