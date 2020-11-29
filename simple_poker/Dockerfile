FROM golang:latest
LABEL maintainer="Alexander Shein (mr.ashein@gmail.com)"

RUN mkdir /goapp
ENV GOPATH=/goapp
ADD . /goapp/src/simple_poker
WORKDIR /goapp/src/simple_poker
RUN go build -o poker_app .
CMD ["/goapp/src/simple_poker/poker_app"]