package main

import (
	"api-gateway-service/internal/config"
	"api-gateway-service/internal/server"
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	cfg, err := config.GetConfig("config/config.yaml")
	if err != nil {
		log.Fatalf("Failed to get config: %v", err)
	}

	srv := server.NewServer(cfg)

	go func() {
		if err := srv.Start(); err != nil && err != http.ErrServerClosed {
			log.Fatalf("Server failed: %v", err)
		}
	}()

	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil{
		log.Fatalf("Server shutdown failed: %v", err)
	}

	log.Println("Server exited")
}
