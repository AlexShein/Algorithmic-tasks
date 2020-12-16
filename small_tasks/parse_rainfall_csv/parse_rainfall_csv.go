package rainfall

import (
	"math"
	"strconv"
	"strings"
)

func parseData(data string) map[string][]float64 {
	res := make(map[string][]float64, 0)
	for _, cityRow := range strings.Split(data, "\n") {
		cityRowProcessed := strings.Split(cityRow, ":")
		cityName, monthsValues := cityRowProcessed[0], cityRowProcessed[1]
		res[cityName] = make([]float64, 0)
		for _, monthAndValueRaw := range strings.Split(monthsValues, ",") {
			monthAndValue := strings.Fields(monthAndValueRaw)
			monthValue, _ := strconv.ParseFloat(monthAndValue[1], 32)
			res[cityName] = append(res[cityName], monthValue)
		}
	}
	return res
}

func mean(values []float64) (intermediate float64) {
	for _, value := range values {
		intermediate += value
	}
	intermediate /= float64(len(values))
	return
}

func variance(values []float64, mean float64) (intermediate float64) {
	for _, value := range values {
		intermediate += math.Pow(value-mean, 2)
	}
	intermediate /= float64(len(values))
	return
}

// Mean computes rainfall mean score based on csv data by city through mean func
func Mean(town string, data string) (result float64) {
	cityToValuesMap := parseData(data)
	if values, ok := cityToValuesMap[town]; ok {
		result = mean(values)
	} else {
		result = -1.0
	}
	return
}

// Variance computes rainfall score variance based on csv data by city through variance func
func Variance(town string, data string) (result float64) {
	cityToValuesMap := parseData(data)
	if values, ok := cityToValuesMap[town]; ok {
		mean := mean(values)
		result = variance(values, mean)
	} else {
		result = -1.0
	}
	return
}
