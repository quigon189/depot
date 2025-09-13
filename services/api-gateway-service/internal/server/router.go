package server

import (
	"net/http"

	"api-gateway-service/internal/handlers/auth"
	"api-gateway-service/internal/handlers/submux"
)

func setupRouter() *http.ServeMux {
	mux := http.NewServeMux()

	authMux := submux.New(mux, "/api/v1/auth")

	auth.SetupAuth(authMux)

	mux.Handle("/health", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))

	return mux
}
