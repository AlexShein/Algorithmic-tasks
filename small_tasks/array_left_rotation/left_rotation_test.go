package leftrotation

import (
	"reflect"
	"testing"
)

type rotationInput struct {
	number int32
	arr    []int32
}

type rotationResult struct {
	input  rotationInput
	output []int32
}

var testCases = []rotationResult{
	{
		input: rotationInput{
			4,
			[]int32{1, 2, 3, 4, 5},
		},
		output: []int32{5, 1, 2, 3, 4},
	},
	{
		input: rotationInput{
			5,
			[]int32{1, 2, 3, 4, 5},
		},
		output: []int32{1, 2, 3, 4, 5},
	},
	{
		input: rotationInput{
			1,
			[]int32{1, 2, 3, 4, 5},
		},
		output: []int32{2, 3, 4, 5, 1},
	},
}

func TestRotateLeft(t *testing.T) {
	for _, testCase := range testCases {
		if funcResult := RotateLeft(testCase.input.number, testCase.input.arr); !reflect.DeepEqual(funcResult, testCase.output) {
			t.Errorf("Input: %v, Expected %v, Got %v", testCase.input, testCase.output, funcResult)
		}
	}
}
