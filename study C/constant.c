#include <stdio.h> //ค่าคงที่
#define ID 101

int main() 
{
    const int BATTERY_MAX = 100; //เปลี่ยนค่าไม่ได้ เพราะใช้ const

    printf("Max battery = %d", BATTERY_MAX);
    return 0;
}