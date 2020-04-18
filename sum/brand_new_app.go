package main

import (
	"fmt"
)

// PositiveSum does something.
func PositiveSum(numbers []int) int {
	result := 0
	for _, value := range numbers {
		if value > 0 {
			result += value
		}
	}
	return result
}

func main() {
	numbers := []int{1, 2, 3, -1, 4, -2}
	fmt.Println(PositiveSum(numbers))

}
