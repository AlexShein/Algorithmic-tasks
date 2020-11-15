package leftrotation

// RotateLeft performs elements rotation 1 2 3 4 5 -> 5 1 2 3 4
func RotateLeft(d int32, arr []int32) []int32 {
	arrLength := int32(len(arr))
	newArr := make([]int32, arrLength)
	for i := int32(0); i < arrLength; i++ {
		newArr[i] = arr[(i+d)%arrLength]
	}
	return newArr
}
