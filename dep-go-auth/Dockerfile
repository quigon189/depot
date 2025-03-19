FROM docker.io/golang:1.24-bookworm AS builder
#FROM docker.io/golang:1.24

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . . 
#RUN CGO_ENABLED=0 GOOS=linux go build -o /server ./cmd/server/main.go

RUN go test ./...

RUN go build -o ./server cmd/server/main.go

FROM docker.io/debian:bookworm-slim
WORKDIR /app

#RUN apk --no-cache add libc6-compat libgcc libstdc++
COPY --from=builder /app/server . 

ENV SECRET_KEY=kuku-epta
EXPOSE 8080

CMD ["./server"]
