package approx

import (
	"math"
)

// EPSILON is a floating point operations accuracy coefficient
const EPSILON = 0.01

// FloatFunc is function type that receives and returns float
type FloatFunc func(float64) float64

// Interp works like map(function, np.linspace(leftBorder, rightBorder, n))
func Interp(function FloatFunc, leftBorder float64, rightBorder float64, n int) (res []float64) {
	step := (rightBorder - leftBorder) / float64(n)
	for i := leftBorder; i < rightBorder-step+EPSILON; i += step {
		res = append(res, math.Floor(function(i)*100)/100)
	}
	return res
}
