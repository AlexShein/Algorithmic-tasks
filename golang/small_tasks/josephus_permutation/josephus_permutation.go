package josephus

// Permutation is a class-like structure to store current state
type Permutation struct {
	items              []interface{}
	resultingIndexes   []int
	currentPosition    int
	unprocessedIndexes []int
	k                  int
}

// PermutationStep adds next element index to resulting indexes slice unless there are no unprocessed elements left
func (pPointer *Permutation) PermutationStep() (done bool, result []interface{}) {
	p := *pPointer
	unprocessedLen := len(p.unprocessedIndexes)
	result = make([]interface{}, 0) // Initialize result to return an empty slice instead of nil in an empty input case
	if unprocessedLen == 0 {
		done = true
		for _, index := range p.resultingIndexes {
			result = append(result, p.items[index])
		}
	} else {
		p.currentPosition = (p.currentPosition + p.k%unprocessedLen - 1) % unprocessedLen
		if p.currentPosition < 0 {
			// Last element of unprocessedIndexes
			p.currentPosition = p.currentPosition + unprocessedLen
		}
		p.resultingIndexes = append(p.resultingIndexes, p.unprocessedIndexes[p.currentPosition])
		p.unprocessedIndexes = append(p.unprocessedIndexes[:p.currentPosition], p.unprocessedIndexes[p.currentPosition+1:]...)
		*pPointer = p
	}
	return
}

// GetPermutation calls PermutationStep until the permutation is done
func (pPointer *Permutation) GetPermutation() (result []interface{}) {
	p := *pPointer
	var done bool
	for true {
		done, result = p.PermutationStep()
		if done {
			break
		}
	}
	return
}

// Josephus returns permutaion of an original array
func Josephus(items []interface{}, k int) (result []interface{}) {
	unprocessedIndexes := []int{}
	for index := range items {
		unprocessedIndexes = append(unprocessedIndexes, index)
	}
	p := Permutation{
		items:              items,
		resultingIndexes:   []int{},
		unprocessedIndexes: unprocessedIndexes,
		k:                  k,
	}
	result = p.GetPermutation()
	return
}
