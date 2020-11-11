package sumofconsecutivearrayelements

import "testing"

type testInput struct {
	input    []int
	expected int
}

var testCases = []testInput{
	testInput{
		input:    []int{-2, 1, -3, 4, -1, 2, 1, -5, 4},
		expected: 6,
	},
	testInput{
		input:    []int{-2, -3, -1},
		expected: 0,
	},
	testInput{
		input:    []int{1, 2, 3, 4, 5},
		expected: 15,
	},
	testInput{
		input:    []int{2, -1, 3, -2, 5},
		expected: 7,
	},
	testInput{
		input:    []int{2},
		expected: 2,
	},
}

func TestMaximumSubarraySum(t *testing.T) {
	for _, testCase := range testCases {
		funcRes := MaximumSubarraySum(testCase.input)
		if funcRes != testCase.expected {
			t.Errorf("Input %v : Expected %d, Got %d\n", testCase.input, testCase.expected, funcRes)
		}
	}
}
