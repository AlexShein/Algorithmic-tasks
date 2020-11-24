package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
	"unicode"
)

type invalidCardError rune

func (card invalidCardError) Error() string {
	return fmt.Sprintf("Invalid card encountered: %s", card)
}

type wrongLengthError string

func (hand wrongLengthError) Error() string {
	return fmt.Sprintf("Wrong hand length: %s", hand)
}

var cardsScoresMap = map[rune]int{
	'2': 101,
	'3': 102,
	'4': 103,
	'5': 104,
	'6': 105,
	'7': 106,
	'8': 107,
	'9': 108,
	'T': 109,
	'J': 110,
	'Q': 111,
	'K': 112,
	'A': 113,
}

const handOneOutcome = "Hand 1"
const handTwoOutcome = "Hand 2"
const tieOutcome = "Tie"

// computeHandScore calculates "score" of cards set so that two sets could be compared using comparison operators < > ==
func computeHandScore(hand [5]rune) (result int) {
	cardsCounts := map[rune]int{}
	for _, card := range hand {
		cardsCounts[card]++
	}
	for card, count := range cardsCounts {
		result += int(math.Pow(float64(cardsScoresMap[card]), float64(count)))
	}
	return
}

func findWinner(handOne [5]rune, handTwo [5]rune) string {
	handOneScore, handTwoScore := computeHandScore(handOne), computeHandScore(handTwo)
	if handOneScore > handTwoScore {
		return handOneOutcome
	} else if handTwoScore > handOneScore {
		return handTwoOutcome
	}
	return tieOutcome
}

func isValidCard(card rune) bool {
	if cardsScoresMap[card] > 0 {
		return true
	}
	return false
}

// convertHand casts passed card set to runes array
// It returns invalidCardError if it encounters non-ASCII/non-card symbol and
// wrongLengthError if card set length is not 5
func convertHand(hand string) ([5]rune, error) {
	result := [5]rune{}
	if len(hand) == 5 {
		for i, card := range hand {
			if card < unicode.MaxASCII && isValidCard(card) {
				result[i] = card
			} else {
				return [5]rune{}, invalidCardError(card)
			}
		}
		return result, nil
	}
	return [5]rune{}, wrongLengthError(hand)
}

// simplePocker wrapps convertation logic and findWinner calls
func simplePocker(rawHand1, rawHand2 string) (string, error) {
	hand1, err := convertHand(rawHand1)
	if err != nil {
		return "", err
	}
	hand2, err := convertHand(rawHand2)
	if err != nil {
		return "", err
	}

	return findWinner(hand1, hand2), nil
}

func main() {
	if len(os.Args[1:]) > 0 && (os.Args[1] == "--help" || os.Args[1] == "-h") {
		fmt.Println("A simple pocker winner finder program.")
		fmt.Println("Developed by A. Shein")
		fmt.Println("Usage: ")
		fmt.Println(`echo 'QQAAJ\n22333' | ./simple_pocker`)
		os.Exit(0)
	}
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Running simple pocker.")
	fmt.Println("Enter first card set: ")
	rawHand1, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	rawHand1 = strings.TrimSuffix(rawHand1, "\n")
	fmt.Println("Enter second card set: ")
	rawHand2, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	rawHand2 = strings.TrimSuffix(rawHand2, "\n")

	winner, err := simplePocker(rawHand1, rawHand2)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("|Hand 1|Hand 2|Winner|")
	fmt.Printf("|%s |%s |%6s|\n", rawHand1, rawHand2, winner)
	os.Exit(0)
}
