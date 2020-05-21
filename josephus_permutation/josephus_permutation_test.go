package josephus

import (
	"reflect"
	"testing"
)

type FuncResult struct {
	input    []interface{}
	k        int
	expected []interface{}
}

var JosephusPermutationResults = []FuncResult{
	{[]interface{}{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, 2, []interface{}{2, 4, 6, 8, 10, 3, 7, 1, 9, 5}},
	{[]interface{}{1, 2, 3, 4, 5, 6, 7}, 3, []interface{}{3, 6, 2, 7, 5, 1, 4}},
	{[]interface{}{}, 3, []interface{}{}},
}

func TestJosephus(t *testing.T) {
	for _, test := range JosephusPermutationResults {
		result := Josephus(test.input, test.k)
		if !reflect.DeepEqual(result, test.expected) {
			t.Errorf("Test failed! Args: %v, Wanted: %v %T, Got: %v %T", test.input, test.expected, test.expected, result, result)
		}
	}
}
