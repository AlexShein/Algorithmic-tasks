package determinant

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	matrix   [][]int
	expected int
}

var DeterminantResults = []FuncResult{
	{[][]int{{1}}, 1},
	{[][]int{{1, 3}, {2, 5}}, -1},
	{[][]int{{2, 5, 3}, {1, -2, -1}, {1, 3, 4}}, -20},
}

func TestDeterminant(t *testing.T) {
	for _, test := range DeterminantResults {
		result := Determinant(test.matrix)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v %T, Got: %v %T", []interface{}{test.matrix}, test.expected, test.expected, result, result)
		}
	}
}
