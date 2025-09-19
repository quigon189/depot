FROM docker.io/golang:alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o api-gateway-service ./cmd/main.go

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/api-gateway-service .
COPY config/podman-config.yaml ./config/config.yaml

EXPOSE 5000

CMD ["./api-gateway-service"]
