package bracketsvalidator

// Bracket type represents a bracket and is meant for logic encapsulation
type Bracket string

var openingBracketsMap = map[Bracket]Bracket{
	"(": ")",
	"[": "]",
	"{": "}",
}
var closingBracketsMap = map[Bracket]Bracket{
	")": "(",
	"]": "[",
	"}": "{",
}

const (
	singleQuote = "'"
	doubleQuote = "\""
)

func (bracket *Bracket) isClosingBracket() bool {
	if _, ok := closingBracketsMap[*bracket]; ok {
		return true
	}
	return false
}

func (bracket *Bracket) isOpeningBracket() bool {
	if _, ok := openingBracketsMap[*bracket]; ok {
		return true
	}
	return false
}

func (bracket *Bracket) isQuote() bool {
	if *bracket == singleQuote || *bracket == doubleQuote {
		return true
	}
	return false
}

func (bracket *Bracket) isValidBracket() bool {
	return bracket.isClosingBracket() || bracket.isOpeningBracket() || bracket.isQuote()
}

func (bracket *Bracket) getMatchingBracket() Bracket {
	if bracket.isOpeningBracket() {
		return openingBracketsMap[*bracket]
	}
	return closingBracketsMap[*bracket]
}

func copyState(state []Bracket) []Bracket {
	newState := make([]Bracket, len(state))
	copy(newState, state)
	return newState
}

func bracketsValidatorInner(input string, state []Bracket) bool {
	for position, symbol := range input {
		if bracket := Bracket(symbol); bracket.isValidBracket() {
			stateLength := len(state)
			if bracket.isQuote() {
				if stateLength == 0 || state[stateLength-1] != bracket {
					state = append(state, bracket)
				} else if state[stateLength-1] == bracket {
					// branch 1: remove last quote bracket, pretend that the one we encountered is a closing one
					newState := copyState(state[:stateLength-1])
					if bracketsValidatorInner(input[position+1:], newState) {
						state = []Bracket{}
						break
					}
					// branch 2: append new quote bracket, consider new one as an opening one
					state = append(state, bracket)
				}
			} else if bracket.isOpeningBracket() {
				state = append(state, bracket)
			} else if stateLength > 0 && state[stateLength-1] == bracket.getMatchingBracket() {
				state = state[:stateLength-1]
			} else {
				return false
			}
		}
	}
	if len(state) == 0 {
		return true
	}
	return false
}

// BracketsValidator valiudates that brackets in the input string are nested and closed correctly
// Let's assume that quotes " ' are kinds of brackets as well, hence we would need
// special logic for those, as they don't have a pair opening-closing variant
func BracketsValidator(input string) bool {
	return bracketsValidatorInner(input, []Bracket{})
}
