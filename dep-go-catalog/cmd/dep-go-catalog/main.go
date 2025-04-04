package main

import (
	"dep-go-catalog/internal/config"
	"log"
)

func main() {
	var cfg config.Config
	cfg.Fetch()

	log.Printf("%+v", cfg)
	log.Fatalf("server %s:%s stoped", cfg.Server.Host, cfg.Server.Port)
}
