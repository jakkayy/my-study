#include <stdio.h> //ตัวแปร
#include <stdbool.h>

int main() 
{
    //student data
    char name[10] = "Nae", gender = 'M';
    int age = 15;
    float gpa = 3.75;
    bool status = false; // false = 0, true = 1

    age = 21;
    gpa = 4.00;

    //output
    printf("Name = %s \n", name);
    printf("age = %d \n", age);
    printf("gender = %c\n", gender);
    printf("gpa = %.2f\n", gpa);
    printf("status = %d", status);
    return 0;
}