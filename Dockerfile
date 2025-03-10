FROM docker.io/golang:1.24-alpine

WORKDIR /app
COPY . ./

RUN go test -v ./...
