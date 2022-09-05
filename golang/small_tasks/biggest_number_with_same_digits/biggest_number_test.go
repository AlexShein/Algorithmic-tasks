package numbers

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	input    int
	expected int
}

var NumberResults = []FuncResult{
	{12, 21},
	{513, 531},
	{2017, 2071},
	{34011, 34101},
	{34111, 43111},
	{531, -1},
	{1, -1},
}

func TestNextBigger(t *testing.T) {
	for _, test := range NumberResults {
		result := NextBigger(test.input)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v, Got: %v", test.input, test.expected, result)
		}
	}
}
