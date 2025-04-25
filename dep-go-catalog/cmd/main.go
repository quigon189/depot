package main

import (
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/database"
	"dep-go-catalog/internal/http"
	"dep-go-catalog/internal/services"
	"fmt"

	"log"
)



func main() {
	cfg := config.FetchConfig()
	log.Printf("%+v", cfg)

	db := database.Connect(cfg)
	database.AutoMigrate(db)

	specService := services.NewSpecService(db)
	
	router := http.NewRouter(
		specService,
	)
	addr := fmt.Sprintf("%s:%s", cfg.Server.Host, cfg.Server.Port)
	log.Printf("Starting server on %s", addr)
	log.Fatal(http.Serve(addr, router))
}
