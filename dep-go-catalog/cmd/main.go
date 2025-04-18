package main

import (
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/database"

	"log"
)


func main() {
	cfg := config.FetchConfig()
	log.Printf("%+v", cfg)

	db := database.Connect(cfg)
	database.AutoMigrate(db)

	log.Fatalf("server %s:%s stoped", cfg.Server.Host, cfg.Server.Port)
}
