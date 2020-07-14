package approx

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	function    FloatFunc
	leftBorder  float64
	rightBorder float64
	n           int
	expected    []float64
}

var InterpResults = []FuncResult{
	{func(input float64) float64 { return input }, 0, 0.9, 3, []float64{0, 0.3, 0.6}},
	{func(input float64) float64 { return input }, 0, 0.9, 4, []float64{0., 0.22, 0.45, 0.67}},
	{func(input float64) float64 { return input }, 0, 15, 9, []float64{0, 1.66, 3.33, 5, 6.66, 8.33, 10, 11.66, 13.33}},
	{func(input float64) float64 { return input + 5 }, 4, 8, 4, []float64{9, 10, 11, 12}},
}

func TestInterp(t *testing.T) {
	for _, test := range InterpResults {
		result := Interp(test.function, test.leftBorder, test.rightBorder, test.n)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v %T, Got: %v %T", []interface{}{test.function, test.leftBorder, test.rightBorder, test.n}, test.expected, test.expected, result, result)
		}
	}
}
