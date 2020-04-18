package main

import (
	"fmt"
	"math"
)

// GetOrderedArraysIntersection receives two arrays with unique elements and returns elements present in both.
func GetOrderedArraysIntersection(arr1 []int, arr2 []int) (result []int) {
	for _, value1 := range arr1 {
		for _, value2 := range arr2 {
			if value2 > value1 {
				break
			} else if value2 == value1 {
				result = append(result, value2)
				break
			}
		}
	}
	return
}

// GetDividers returns list of unique dividers of a number.
func GetDividers(num int) (result []int) {
	for i := 2; i <= int(math.Sqrt(float64(num))); i++ {
		if num%i == 0 {
			num /= i
			result = append(result, i)
			for true {
				if num%i == 0 {
					num /= i
				} else {
					break
				}
			}
		}
		if num == 1 {
			break
		}
	}
	return
}

// Max selects largest integer of two provided values.
func Max(x, y int) int {
	if x < y {
		return y
	}
	return x
}

// Min selects smallest integer of two provided values.
func Min(x, y int) int {
	if x > y {
		return y
	}
	return x
}

// SumFracts addresses the kata task - returns irreducible sum of rationals.
func SumFracts(arr [][]int) string {
	fmt.Println("Solving: ", arr)
	var resNum, resDen int = 0, 1
	for _, values := range arr {
		num := values[0]
		den := values[1]
		resNum = resNum*den + num*resDen
		resDen = resDen * den
		commonDividers := GetOrderedArraysIntersection(
			GetDividers(resNum),
			GetDividers(resDen),
		)
		for _, divider := range commonDividers {
			for true {
				if resNum%divider == 0 && resDen%divider == 0 {
					resNum /= divider
					resDen /= divider
				} else {
					break
				}
			}
		}

	}
	if resNum%resDen == 0 {
		return fmt.Sprint(resNum / resDen)
	}
	return fmt.Sprintf("%d/%d", resNum, resDen)
}

func main() {
	var numbers [][]int
	fmt.Println("Starting")
	numbers = [][]int{{1, 2}, {1, 3}, {1, 4}}
	fmt.Println("First")
	fmt.Println(SumFracts(numbers))
	numbers = [][]int{{1, 3}, {5, 3}}
	fmt.Println("Second")
	fmt.Println(SumFracts(numbers))
	numbers = [][]int{{1, 8}, {2, 5}, {7, 8}}
	fmt.Println(SumFracts(numbers))
	fmt.Println("Third")
	numbers = [][]int{{166, 165}}
	fmt.Println(SumFracts(numbers))
	fmt.Println("Forth")
	numbers = [][]int{{81345, 15786}, {87546, 11111111}, {43216, 255689}}
	fmt.Println(SumFracts(numbers))
	fmt.Println("Fifth")
	fmt.Println("Done!")

}
