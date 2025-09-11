package main

import (
	"auth-service/internal/config"
	"auth-service/internal/database"
	"auth-service/internal/server"
	"auth-service/internal/service"
	"log"
	"os"
	"os/signal"
	"syscall"
)

func main() {
	cfg, err := config.GetConfig("config/config.yaml")
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	db, err := database.NewPostresDB(&cfg.Database)
	if err != nil {
		log.Fatalf("Failed to connect to DB: %v", err)
	}
	defer db.Close()

	authService := service.NewAuthService(
		db,
		cfg.JWT.Secret,
		cfg.JWT.RefreshTokenExpiry,
		cfg.JWT.RefreshTokenExpiry,
	)

	grpcServer := server.NewGRPCServer(cfg, authService)

	go func() {
		if err := grpcServer.Start(); err != nil {
			log.Fatalf("Failed to start gRPC server: %v", err)
		}
	}()

	log.Println("Auth Service started successfuly")

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down gRPC server...")
	grpcServer.Stop()
	log.Println("Server exited")
}
