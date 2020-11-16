package cookies

import (
	"sort"
)

func insertNew(newCookie int32, cookiesSlice []int32) []int32 {
	position := sort.Search(
		len(cookiesSlice),
		func(i int) bool {
			return cookiesSlice[i] >= newCookie
		},
	)
	remainingCookies := make([]int32, len(cookiesSlice[position:]))
	copy(remainingCookies, cookiesSlice[position:])
	return append(append(cookiesSlice[0:position], newCookie), remainingCookies...)
}

//Cookies returns minimum operations required to obtain desired sweetness.
//https://www.hackerrank.com/challenges/jesse-and-cookies/problem
func Cookies(k int32, cookiesSlice []int32) int32 {
	var result int32 = 0
	sort.Slice(
		cookiesSlice,
		func(i, j int) bool { return cookiesSlice[i] < cookiesSlice[j] },
	)
	for true {
		if cookiesSlice[0] >= k {
			break
		}
		if len(cookiesSlice) < 2 {
			result = -1
			break
		}
		cookiesSlice = insertNew(
			cookiesSlice[0]+2*cookiesSlice[1], cookiesSlice[2:],
		)
		result++
	}
	return result
}
