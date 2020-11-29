# Simple pocker command line app

## General information:

This program reads two card sets from `stdin` and prints a winner, which is always one of ["Hand 1", "Hand 2", "Tie"].
It was developed and tested using Go version `1.14.2`.

## Building and running without Docker:

Please, ensure that you have Go installed on your machine.
First, you need to build this program from sources:

1. Place source code folder to `$GOPATH/src`
2. Change directory to `$GOPATH/src/simple_pocker/`
3. Run `go build`

You can run `$GOPATH/src/simple_pocker/simple_pocker` either in an interactive mode (you'll be prompted to enter card sets separated by new line)
or pass card sets to the program using e.g. `echo` command: `echo 'QQAAJ\n22333' | ./simple_pocker`

Help is acessible via running `simple_pocker` with `--help` argument.

## Building and running using Docker:

Please, ensure that you have Docker installed on your machine.
These steps was tested using Docker version `19.03.13`.

1. Build and tag the docker image using `docker build . --tag simple_pocker:0.1`
2. Run it in an interactive mode: `docker run -it simple_pocker:0.1` OR pass cards sets using e.g. `echo`: `echo 'QQAAJ\n22333' | docker run -i simple_pocker:0.1`

## Additional info:

This package contains unit tests (`simple_pocker/simple_pocker_test.go`).
You may need to install `github.com/stretchr/testify/assert` testing package prior to running them.
Since this project contains `go.mod` file, running `go test` will be install the required package as well as run tests.
