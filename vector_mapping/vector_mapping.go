package main

import (
	"fmt"
	"math"
)

// EPS is the default accuracy for float numbers comparison.
var EPS float64 = 0.0000001

// FromPolar maps polar to cartesian coordinates.
func FromPolar(r, phi float64) (x, y float64) {
	x = r * math.Cos(phi)
	y = r * math.Sin(phi)
	return
}

// ToPolar maps cartesian to polar coordinates.
func ToPolar(x, y float64) (r, phi float64) {
	phi = 0
	r = math.Sqrt(x*x + y*y)
	if x > 0 && y >= 0 {
		phi = math.Atan(y / x)
	} else if x > 0 && y < 0 {
		phi = math.Atan(y/x) + 2*math.Pi
	} else if x < 0 {
		phi = math.Atan(y/x) + math.Pi
	} else if math.Abs(x) < EPS {
		if y > 0 {
			phi = math.Pi / 2
		} else if y < 0 {
			phi = math.Pi * 3 / 2
		}
	}
	return
}

// MapVector maps vector from circle1 to circle2.
func MapVector(vector, circle1, circle2 []float64) []float64 {
	// Project vector on the plane relative to circle 1 center as zero point
	x, y := vector[0]-circle1[0], vector[1]-circle1[1]
	radiiRatio := circle2[2] / circle1[2]
	r, phi := ToPolar(x, y)
	r = r * radiiRatio
	x, y = FromPolar(r, phi)
	// Project vector on the plane relative to 0, 0 as zero point again
	x, y = x+circle2[0], y+circle2[1]
	return []float64{x, y}
}

func main() {
	fmt.Println("Starting")
	fmt.Println("Res1", MapVector([]float64{46, 58}, []float64{0, 0, 100}, []float64{0, 0, 100}))
	fmt.Println("Res2", MapVector([]float64{1, 1}, []float64{0, 0, 2}, []float64{0, 0, 4}))
	fmt.Println("Res3", MapVector([]float64{1, 1}, []float64{0, 0, 2}, []float64{1, 1, 4}))
	fmt.Println("Res4", MapVector([]float64{1.5, 1.5}, []float64{2, 2, 1}, []float64{2, -2, 1}))
	fmt.Println("Done!")
}
