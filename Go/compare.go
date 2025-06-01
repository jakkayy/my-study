package main

import "fmt"

func main() {
	num1, num2 := 10, 3
	fmt.Println("เท่ากันหรือไม่ =", num1 == num2)
	fmt.Println("ไม่เท่ากันหรือไม่ =", num1 != num2)
	fmt.Println("num1 มากกว่าหรือไม่ =", num1 >= num2)
	fmt.Println("num2 มากกว่าหรือไม่ =", num1 <= num2)
}
