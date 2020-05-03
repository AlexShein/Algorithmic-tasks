package mergedsort

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	input    []int
	expected []int
}

var MergedSortResults = []FuncResult{
	{[]int{0}, []int{0}},
	{[]int{1, 2, 3}, []int{3, 2, 1}},
	{[]int{1, 3, 2, 4}, []int{4, 3, 2, 1}},
	{[]int{4, 2, 3, 1, 6, 5, 7}, []int{7, 6, 5, 4, 3, 2, 1}},
}

func TestMergedSort(t *testing.T) {
	for _, test := range MergedSortResults {
		result := MergedSort(test.input)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v, Got: %v", test.input, test.expected, result)
		}
	}
}
