package cons

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	input    string
	expected int
}

var ConsonantValueResults = []FuncResult{
	{"a", 0},
	{"ab", 2},
	{"strength", 57},
}

func TestConsonantValue(t *testing.T) {
	for _, test := range ConsonantValueResults {
		result := ConsonantValue(test.input)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v, Got: %v", test.input, test.expected, result)
		}
	}
}
