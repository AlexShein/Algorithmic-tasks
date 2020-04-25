package parse

// Parse solves the kata's task
func Parse(input string) (res []int) {
	buffer := 0
	res = []int{}
	for _, command := range input {
		switch command {
		case 'i':
			buffer++
		case 'd':
			buffer--
		case 's':
			buffer *= buffer
		case 'o':
			res = append(res, buffer)
		}
	}
	return
}
