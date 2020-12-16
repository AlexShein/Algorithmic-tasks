package mergedsort

// MergedSort implements a merged sort algorithm
func MergedSort(vals []int) (result []int) {
	length := len(vals)
	if length == 1 {
		return vals
	}
	middle := length / 2
	arr1, arr2 := MergedSort(vals[:middle]), MergedSort(vals[middle:])
	arr1Index, arr2Index := 0, 0
	arr1Length, arr2Length := len(arr1), len(arr2)
	for i := 0; i < (len(arr1) + len(arr2)); i++ {
		if (arr1Index < arr1Length) && (arr2Index < arr2Length) {
			if arr1[arr1Index] > arr2[arr2Index] {
				result = append(result, arr1[arr1Index])
				arr1Index++
			} else {
				result = append(result, arr2[arr2Index])
				arr2Index++
			}
		} else if arr1Index < arr1Length {
			result = append(result, arr1[arr1Index])
			arr1Index++
		} else {
			result = append(result, arr2[arr2Index])
			arr2Index++
		}
	}
	return
}
