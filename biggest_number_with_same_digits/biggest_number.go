package numbers

import (
	"strconv"
	"strings"
)

func toArray(number int) (res []int) {
	strRep := strconv.Itoa(number)
	strArr := strings.Split(strRep, "")
	for _, val := range strArr {
		intRepr, _ := strconv.Atoi(val)
		res = append(res, intRepr)
	}
	return
}

func fromArray(numbers []int) (res int) {
	strArr := []string{}
	for _, number := range numbers {
		strRep := strconv.Itoa(number)
		strArr = append(strArr, strRep)
	}
	res, _ = strconv.Atoi(strings.Join(strArr, ""))
	return
}

// NextBigger returns next bigger number made up from the same digits
func NextBigger(n int) int {
	arrRepr := toArray(n)
	for i := len(arrRepr) - 2; i >= 0; i-- {
		if arrRepr[i+1] > arrRepr[i] {
			arrRepr[i+1], arrRepr[i] = arrRepr[i], arrRepr[i+1]
			return fromArray(arrRepr)
		}
	}
	return -1
}
