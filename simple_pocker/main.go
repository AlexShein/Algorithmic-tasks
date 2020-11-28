package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

func main() {
	if len(os.Args[1:]) > 0 && (os.Args[1] == "--help" || os.Args[1] == "-h") {
		fmt.Println("A simple pocker winner finder program.")
		fmt.Println("Developed by A. Shein")
		fmt.Println("Usage: ")
		fmt.Println(`echo 'QQAAJ\n22333' | ./simple_pocker`)
		os.Exit(0)
	}
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Running simple pocker.")
	fmt.Println("Enter first card set: ")
	rawHand1, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	rawHand1 = strings.TrimSuffix(rawHand1, "\n")
	fmt.Println("Enter second card set: ")
	rawHand2, err := reader.ReadString('\n')
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	rawHand2 = strings.TrimSuffix(rawHand2, "\n")

	winner, err := simplePocker(rawHand1, rawHand2)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	fmt.Println("|Hand 1|Hand 2|Winner|")
	fmt.Printf("|%s |%s |%6s|\n", rawHand1, rawHand2, winner)
	os.Exit(0)
}
