package sumofconsecutivearrayelements

func maxOfTwo(first int, second int) int {
	if first > second {
		return first
	}
	return second
}

// MaximumSubarraySumSimplified finds maximum sum of consecutive elements in the input array
func MaximumSubarraySumSimplified(numbers []int) (res int) {
	sumAcc := 0
	for _, i := range numbers {
		sumAcc += i
		res = maxOfTwo(res, sumAcc)
		sumAcc = maxOfTwo(sumAcc, 0)
	}
	return
}

func max(values []int) (res int) {
	for _, value := range values {
		if value > res {
			res = value
		}
	}
	return
}

// MaximumSubarraySum finds maximum sum of consecutive elements in the input array
func MaximumSubarraySum(inputArray []int) (res int) {
	intermediateResults := []int{}

	for _, current := range inputArray {
		stepResults := []int{}
		nextStepIntermediateResults := []int{}
		for _, intermediate := range intermediateResults {
			currentSum := intermediate + current
			if currentSum > 0 {
				// If sum of current element and perviously added ones
				// (either previous element, or sum of several prevoius ones)
				// is bigger than 0, than we should continue processing of those elements
				nextStepIntermediateResults = append(nextStepIntermediateResults, currentSum)
				stepResults = append(stepResults, intermediate)
				stepResults = append(stepResults, currentSum)
			}
		}
		if current > 0 {
			// current element alone may be be the largest possible sum of elements
			stepResults = append(stepResults, current)
			nextStepIntermediateResults = append(nextStepIntermediateResults, current)
		}
		intermediateResults = nextStepIntermediateResults

		stepResult := max(stepResults)
		if stepResult > res {
			res = stepResult
		}
	}
	return
}
