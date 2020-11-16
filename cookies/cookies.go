package cookies

import (
	"container/heap"
)

// An Item is something we manage in a priority queue.
type Item struct {
	value    int64 // The value of the item; arbitrary.
	priority int64 // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	return pq[i].priority < pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

// Push is required by heap's interface
func (pq *PriorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

// Pop is required by heap's interface as well
func (pq *PriorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

//Cookies returns minimum operations required to obtain desired sweetness.
//https://www.hackerrank.com/challenges/jesse-and-cookies/problem
//The priority queue implementation was proudly copypasted from
//https://golang.org/pkg/container/heap/
func Cookies(k int32, cookiesSlice []int32) int32 {
	pq := make(PriorityQueue, len(cookiesSlice))
	for i, sweetness := range cookiesSlice {
		pq[i] = &Item{
			value:    int64(sweetness),
			priority: int64(sweetness),
			index:    i,
		}
		i++
	}
	heap.Init(&pq)

	var result int32 = 0
	for true {
		if pq[0].value >= int64(k) {
			break
		}
		if pq.Len() < 2 {
			result = -1
			break
		}
		leastSweetCookie := *heap.Pop(&pq).(*Item)
		secondLeastSweetCookie := *heap.Pop(&pq).(*Item)
		sweetness := leastSweetCookie.priority + 2*secondLeastSweetCookie.priority
		heap.Push(&pq, &Item{
			value:    sweetness,
			priority: sweetness,
		})
		result++
	}
	return result
}
