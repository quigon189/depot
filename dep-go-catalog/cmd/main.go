package main

import (
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/database"
	"dep-go-catalog/internal/http"
	"dep-go-catalog/internal/services"
	"net"

	"log"
)



func main() {
	cfg := config.FetchConfig()
	//log.Printf("%+v", cfg)

	db := database.Connect(cfg)
	database.AutoMigrate(db)

	specService := services.NewSpecService(db)
	groupService := services.NewGroupService(db, specService)
	
	router := http.NewRouter(
		specService,
		groupService,
	)
	
	addr := net.JoinHostPort(cfg.Server.Host, cfg.Server.Port)
	log.Printf("Starting server on %s", addr)
	log.Fatal(http.Serve(addr, router))
}
