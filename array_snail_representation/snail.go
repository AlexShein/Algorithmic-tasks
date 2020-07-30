package snail

var directions = [4][2]int{
	{0, 1},
	{1, 0},
	{0, -1},
	{-1, 0},
}

// DirectionsGenerator is a class-like structure of direction arrays with a single method GetNextDirection which emulates a generator
type DirectionsGenerator struct {
	position int
}

// GetNextDirection returns next direction depending on directions order
func (dgPointer *DirectionsGenerator) GetNextDirection() [2]int {
	dg := *dgPointer
	result := directions[dg.position]
	dg.position = (dg.position + 1) % 4
	*dgPointer = dg
	return result
}

// Solver is a class-like structure to solve snail kata
type Solver struct {
	directionsGenerator DirectionsGenerator
	dataArray           [][]int
	currentPosition     [2]int
	bordersX            [2]int
	bordersY            [2]int
	result              []int
}

func (solverPointer *Solver) step() (done bool) {
	solver := *solverPointer

	if solver.bordersX[1]-solver.bordersX[0] == 0 &&
		solver.bordersY[1]-solver.bordersY[0] == 0 {
		// Append last element to the result
		solver.result = append(solver.result, solver.dataArray[solver.bordersY[0]][solver.bordersX[0]])
		*solverPointer = solver
		return true
	}

	direction := solver.directionsGenerator.GetNextDirection()
	// We should move current position and append elements to result until we reach either x or y border of unprocessed array part
	for true {
		// Changing current position according to our moving direction
		solver.currentPosition[0] += direction[0]
		solver.currentPosition[1] += direction[1]

		solver.result = append(solver.result, solver.dataArray[solver.currentPosition[0]][solver.currentPosition[1]])
		if direction[1] > 0 && (solver.currentPosition[1] == solver.bordersX[1]) ||
			direction[1] < 0 && (solver.currentPosition[1] == solver.bordersX[0]) ||
			direction[0] > 0 && (solver.currentPosition[0] == solver.bordersY[1]) ||
			direction[0] < 0 && (solver.currentPosition[0] == solver.bordersY[0]) {
			break
		}
	}
	// Changing borders of an array for next iteration depending on which row or column was processed
	if direction[1] > 0 {
		solver.bordersY[0] = solver.bordersY[0] + direction[1]
	} else if direction[1] < 0 {
		solver.bordersY[1] = solver.bordersY[1] + direction[1]
	} else if direction[0] > 0 {
		solver.bordersX[1] = solver.bordersX[1] - direction[0]
	} else {
		solver.bordersX[0] = solver.bordersX[0] - direction[0]
	}

	*solverPointer = solver
	return false
}

// Snail flattens input 2d matrix and returns it's elements in a specific order
// array = [[1,2,3],
//          [8,9,4],
//          [7,6,5]]
// snail(array) #=> [1,2,3,4,5,6,7,8,9]
func Snail(snailMatrix [][]int) []int {
	if !(len(snailMatrix) == 1 && len(snailMatrix[0]) == 0) {
		solver := Solver{
			directionsGenerator: DirectionsGenerator{position: 0},
			dataArray:           snailMatrix,
			currentPosition:     [2]int{0, -1},
			bordersX:            [2]int{0, len(snailMatrix) - 1},
			bordersY:            [2]int{0, len(snailMatrix[0]) - 1},
		}
		for true {
			done := solver.step()
			if done {
				return solver.result
			}
		}
	}
	return []int{}
}
