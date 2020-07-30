package snail

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	array    [][]int
	expected []int
}

var SnailResults = []FuncResult{
	{[][]int{{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}, []int{1, 2, 3, 6, 9, 8, 7, 4, 5}},
	{[][]int{{1, 2, 3, 1}, {4, 5, 6, 4}, {7, 8, 9, 7}, {7, 8, 9, 7}}, []int{1, 2, 3, 1, 4, 7, 7, 9, 8, 7, 7, 4, 5, 6, 9, 8}},
	{[][]int{{}}, []int{}},
}

func TestSnail(t *testing.T) {
	for _, test := range SnailResults {
		result := Snail(test.array)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v %T, Got: %v %T", test.array, test.expected, test.expected, result, result)
		}
	}
}

var directionsResults = [][2]int{
	{0, 1},
	{1, 0},
	{0, -1},
	{-1, 0},
	{0, 1},
	{1, 0},
	{0, -1},
	{-1, 0},
}

func TestDirections(t *testing.T) {
	dg := DirectionsGenerator{position: 0}
	for _, expectedResult := range directionsResults {
		result := dg.GetNextDirection()
		if !reflect.DeepEqual(result, expectedResult) {
			t.Errorf("Test failed! Wanted: %v %T, Got: %v %T", expectedResult, expectedResult, result, result)
		}
	}
}
