package main

import (
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/database"
	"dep-go-catalog/internal/http"
	"net"

	"log"
)

func main() {
	cfg := config.FetchConfig()
	//log.Printf("%+v", cfg)

	db := database.Connect(cfg)
	database.AutoMigrate(db)

	addr := net.JoinHostPort(cfg.Server.Host, cfg.Server.Port)

	server := http.NewServer(db, addr)
	log.Printf("Starting server on %s", addr)
	log.Fatal(server.Serve())
}
