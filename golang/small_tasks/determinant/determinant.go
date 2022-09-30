package determinant

import (
	"math"
)

func Determinant(matrix [][]int) (res int) {
	if len(matrix) == 1 {
		return matrix[0][0]
	}
	if len(matrix) == 2 {
		return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
	}
	for index, value := range matrix[0] {
		subArr := [][]int{}
		for i := range matrix[1:] {
			row := []int{}
			for j := range matrix[i] {
				if j != index {
					row = append(row, matrix[i+1][j])
				}
			}
			subArr = append(subArr, row)
		}
		res += value * int(math.Pow(-1, float64(index))) * Determinant(subArr)
	}
	return
}
