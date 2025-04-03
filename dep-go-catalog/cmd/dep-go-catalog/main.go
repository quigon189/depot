package main

import (
	"dep-go-catalog/internal/config"
	"log"
)

func main() {
	cfg := config.Fetch()
	log.Printf("%+v", cfg)
	log.Fatalf("server %s:%s stoped", cfg.Server.Host, cfg.Server.Port)
}
