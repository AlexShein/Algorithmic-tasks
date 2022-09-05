package cons

import "strings"

const vovels = "aeiou"
const asciiOffset = int('a')

// ConsonantValue retrun sum of maximum consonants sequence ascii codes normed to 'a' letter offset
func ConsonantValue(input string) (maxSum int) {
	currentSum := 0
	for _, char := range input {
		if strings.Contains(vovels, string(char)) {
			currentSum = 0
		} else {
			currentSum += int(char) - asciiOffset + 1
		}
		if currentSum > maxSum {
			maxSum = currentSum
		}
	}
	return
}
