FROM golang:latest
LABEL maintainer="Alexander Shein (mr.ashein@gmail.com)"

RUN mkdir /goapp
ENV GOPATH=/goapp
ADD . /goapp/src/simple_pocker
WORKDIR /goapp/src/simple_pocker
RUN go build -o pocker_app .
CMD ["/goapp/src/simple_pocker/pocker_app"]