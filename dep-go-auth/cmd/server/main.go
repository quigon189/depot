package main

import (
	"db-go-auth/internal/config"
	"db-go-auth/internal/server"
	"log"
)

func main() {

	cfg := config.Fetch()

	if cfg.Server.Secret == "" {
		log.Fatalf("SECRET_KEY is not set in config file")
	}

	log.Fatal(server.StartServer(
		"app.db",
		cfg.Server.Host,
		cfg.Server.Port,
		cfg.Server.Secret,
	))
}
