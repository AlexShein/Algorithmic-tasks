package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type simplePockerInput struct {
	handOne string
	handTwo string
}

type simplePockerResult struct {
	input  simplePockerInput
	output string
	err    error
}

var simplePockerTestCases = []simplePockerResult{
	{
		input: simplePockerInput{
			handOne: "AQAQA",
			handTwo: "AQAQ2",
		},
		output: handOneOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "55223",
			handTwo: "44332",
		},
		output: handOneOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "99965",
			handTwo: "99975",
		},
		output: handTwoOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "22234",
			handTwo: "99876",
		},
		output: handOneOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AKQJT",
			handTwo: "22345",
		},
		output: handTwoOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AAKKQ",
			handTwo: "22233",
		},
		output: handTwoOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AA223",
			handTwo: "KKQQJ",
		},
		output: handOneOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AAAKK",
			handTwo: "22223",
		},
		output: handTwoOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "32322",
			handTwo: "AKAKA",
		},
		output: handTwoOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AAQQT",
			handTwo: "TAQAQ",
		},
		output: tieOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "23456",
			handTwo: "36425",
		},
		output: tieOutcome,
		err:    nil,
	},
	{
		input: simplePockerInput{
			handOne: "AKQJ",
			handTwo: "22345",
		},
		output: "",
		err:    wrongLengthError(""),
	},
	{
		input: simplePockerInput{
			handOne: "DKQJA",
			handTwo: "22345",
		},
		output: "",
		err:    invalidCardError('D'),
	},
	{
		input: simplePockerInput{
			handOne: "йQQAAT", // the card set includes unicode character, hence string's length will be larger than 5
			handTwo: "22345",
		},
		output: "",
		err:    wrongLengthError(""),
	},
	{
		input: simplePockerInput{
			handOne: "йQQA", // this card set includes unicode character as well, but it's len() will be exactly 5
			handTwo: "22345",
		},
		output: "",
		err:    invalidCardError('й'),
	},
}

func TestFindWinner(t *testing.T) {
	for _, testCase := range simplePockerTestCases {
		funcResult, err := simplePocker(testCase.input.handOne, testCase.input.handTwo)
		assert.Equal(t, testCase.output, funcResult, testCase.input)
		assert.IsType(t, err, testCase.err)
	}
}
