FROM docker.io/golang:1.24-bookworm AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o ./server cmd/main.go

FROM docker.io/debian:bookworm-slim
WORKDIR /app

COPY --from=builder /app/server .
COPY --from=builder /app/config.yml .

EXPOSE 8080

CMD ["./server"]
