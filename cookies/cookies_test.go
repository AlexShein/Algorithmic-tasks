package cookies

import "testing"

type cookiesInput struct {
	minSweetness int32
	arr          []int32
}

type cookiesResult struct {
	input  cookiesInput
	output int32
}

var testCases = []cookiesResult{
	{
		input: cookiesInput{
			7,
			[]int32{1, 2, 3, 9, 10, 12},
		},
		output: 2,
	},
	{
		input: cookiesInput{
			90,
			[]int32{13, 47, 74, 12, 89, 74, 18, 38},
		},
		output: 5,
	},
	{
		input: cookiesInput{
			15,
			[]int32{1, 2, 3},
		},
		output: -1,
	},
	{
		input: cookiesInput{
			10,
			[]int32{10, 20, 30},
		},
		output: 0,
	},
}

func TestCookies(t *testing.T) {
	for _, testCase := range testCases {
		if funcResult := Cookies(testCase.input.minSweetness, testCase.input.arr); funcResult != testCase.output {
			t.Errorf("Input: %v, Expected %v, Got %v", testCase.input, testCase.output, funcResult)
		}
	}
}
