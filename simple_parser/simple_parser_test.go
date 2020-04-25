package parse

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	input    string
	expected []int
}

var ParseResults = []FuncResult{
	{"o", []int{0}},
	{"io", []int{1}},
	{"iiio", []int{3}},
	{"idoidoiio", []int{0, 0, 2}},
	{"iisoidoiso", []int{4, 4, 25}},
	{"", []int{}},
}

func TestParse(t *testing.T) {
	for _, test := range ParseResults {
		result := Parse(test.input)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v, Got: %v", test.input, test.expected, result)
		}
	}
}
