#include <stdio.h> //รับข้อมูล

int main() 
{
    //data
    char name[10], gender;
    int age;
    float gpa;

    //input
    printf("Input Name = ");
    scanf("%s", &name);
    printf("Input Age = ");
    scanf("%d", &age);
    printf("Input gender = ");
    scanf(" %c", &gender);
    printf("Input gpa = ");
    scanf("%f", &gpa);

    //output
    printf("-------------------\n");
    printf("Name = %s\n", name);
    printf("Age = %d\n", age);
    printf("Gender = %c\n", gender);
    printf("gpa = %.2f\n", gpa);

    return 0;
}