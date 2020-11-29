package main

import (
	"fmt"
	"sort"
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
	'2': 2,
	'3': 3,
	'4': 4,
	'5': 5,
	'6': 6,
	'7': 7,
	'8': 8,
	'9': 9,
	'T': 10,
	'J': 11,
	'Q': 12,
	'K': 13,
	'A': 14,
}

const (
	handOneOutcome = "Hand 1"
	handTwoOutcome = "Hand 2"
	tieOutcome     = "Tie"
)
const (
	higherComparissonOutcome = 1
	lowerComparissonOutcome  = -1
	equalComparissonOutcome  = 0
)

type cardsHand [5]rune

func (hand *cardsHand) getCountsMap() map[rune]int {
	result := map[rune]int{}
	for _, card := range hand {
		result[card]++
	}
	return result
}

// getIsCardLess returns a "less" function for two cards with cards array and cards counts passed as arguments
func getIsCardLess(cards []rune, cardsCountsMap map[rune]int) func(i, j int) bool {
	return func(i, j int) bool {
		leftCard, rightCard := cards[i], cards[j]
		return cardsCountsMap[leftCard] > cardsCountsMap[rightCard] || (cardsCountsMap[leftCard] == cardsCountsMap[rightCard] &&
			cardsScoresMap[leftCard] > cardsScoresMap[rightCard])
	}
}

/*
compare incapsulates card sets comparisson logic: it calculates card counts in each hand
and sorts them by counts and by cards scores (A has the highest, 2 - lowest).
The final step is to iterate over both converted sets and to compare cards scores and counts.
*/
func (hand *cardsHand) compare(otherHand cardsHand) int {
	leftCountsMap := hand.getCountsMap()
	leftCardsUnique := make([]rune, 0, len(leftCountsMap))
	for key := range leftCountsMap {
		leftCardsUnique = append(leftCardsUnique, key)
	}
	sort.Slice(leftCardsUnique, getIsCardLess(leftCardsUnique, leftCountsMap))

	rightCountsMap := otherHand.getCountsMap()
	rightCardsUnique := make([]rune, 0, len(rightCountsMap))
	for key := range rightCountsMap {
		rightCardsUnique = append(rightCardsUnique, key)
	}
	sort.Slice(rightCardsUnique, getIsCardLess(rightCardsUnique, rightCountsMap))

	for i, j := 0, 0; i < len(leftCardsUnique) && j < len(rightCardsUnique); {
		leftCard, rightCard := leftCardsUnique[i], rightCardsUnique[j]
		if leftCountsMap[leftCard] > rightCountsMap[rightCard] {
			return higherComparissonOutcome
		} else if leftCountsMap[leftCard] < rightCountsMap[rightCard] {
			return lowerComparissonOutcome
		} else if leftCountsMap[leftCard] == rightCountsMap[rightCard] && cardsScoresMap[leftCard] > cardsScoresMap[rightCard] {
			return higherComparissonOutcome
		} else if leftCountsMap[leftCard] == rightCountsMap[rightCard] && cardsScoresMap[leftCard] < cardsScoresMap[rightCard] {
			return lowerComparissonOutcome
		}
		i++
		j++
	}
	return equalComparissonOutcome
}

func findWinner(handOne, handTwo cardsHand) string {
	comparissonResult := handOne.compare(handTwo)
	if comparissonResult == higherComparissonOutcome {
		return handOneOutcome
	} else if comparissonResult == lowerComparissonOutcome {
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

// convertHand casts passed card set to cardsHand
// It returns invalidCardError if it encounters non-ASCII/non-card symbol and
// wrongLengthError if card set length is not 5
func convertHand(hand string) (cardsHand, error) {
	result := cardsHand{}
	if len(hand) == 5 {
		for i, card := range hand {
			if card < unicode.MaxASCII && isValidCard(card) {
				result[i] = card
			} else {
				return cardsHand{}, invalidCardError(card)
			}
		}
		return result, nil
	}
	return cardsHand{}, wrongLengthError(hand)
}

// simplePoker wrapps convertation logic and findWinner call
func simplePoker(rawHand1, rawHand2 string) (string, error) {
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
