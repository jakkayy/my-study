package main

import "fmt"

//นิยามตัวแปร
func main() {
	const name string = "jakkaphan" //ค่าคงที่
	lastname := "sirirat"
	var age int = 21
	var score float32 = 77.5
	var isPass bool = true
	fmt.Println("My name is", name)
	fmt.Println("My lastname is", lastname)
	fmt.Println("Age :", age)
	fmt.Println("Score :", score)
	fmt.Println("Pass exaam :", isPass)
}
