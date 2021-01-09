package bracketsvalidator

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type bracketsValidatorResult struct {
	input  string
	output bool
}

var testCases = []bracketsValidatorResult{
	{
		input:  "{[]()}",
		output: true,
	},
	{
		input:  "{}[]()",
		output: true,
	},
	{
		input:  "{}[()]()",
		output: true,
	},
	{
		input:  "((()))",
		output: true,
	},
	{
		input:  "{[(])}",
		output: false,
	},
	{
		input:  "",
		output: true,
	},
	{
		input:  "(",
		output: false,
	},
	{
		input:  ")",
		output: false,
	},
	{
		input:  "\"[]\"",
		output: true,
	},
	{
		input:  "\"''\"",
		output: true,
	},
	{
		input:  "\"'()'\"",
		output: true,
	},
	{
		input:  "''",
		output: true,
	},
	{
		input:  "''''",
		output: true,
	},
	{
		input:  "''[]''",
		output: true,
	},
	{
		input:  "''[''",
		output: false,
	},
}

func TestBracketsValidator(t *testing.T) {
	for _, testCase := range testCases {
		funcResult := BracketsValidator(testCase.input)
		assert.Equal(t, testCase.output, funcResult, testCase.input)
	}
}
