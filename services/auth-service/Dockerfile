FROM docker.io/golang:alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o auth-service ./cmd/main.go

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/auth-service .
COPY --from=builder /app/migrations ./migrations
COPY config/podman-config.yaml ./config/config.yaml

EXPOSE 50051

CMD ["./auth-service"]
