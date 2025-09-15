package server

import (
	"log"
	"net/http"

	"api-gateway-service/internal/config"
	"api-gateway-service/internal/handlers/auth"
	"api-gateway-service/internal/handlers/submux"
)

func setupRouter(cfg *config.Config) *http.ServeMux {
	mux := http.NewServeMux()

	authMux := submux.New(mux, "/api/v1/auth")

	err := auth.SetupAuth(cfg.GRPCServices.Auth, authMux)
	if err != nil {
		log.Fatalf("Failed to setup auth handlers: %v", err)
	}

	mux.Handle("/health", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))

	return mux
}
