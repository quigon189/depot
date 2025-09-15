package auth

import (
	"api-gateway-service/internal/config"
	"api-gateway-service/internal/grpc/auth_grpc"
	"api-gateway-service/internal/handlers/submux"
	"encoding/json"
	"net/http"
)

func SetupAuth(mux *submux.SubMux) {
	authHandler := NewAuthHandler(cfg)
	mux.HandleFunc("/login POST", authHandler.Login)
}

type AuthHandler struct {
	grpcClient *GRPCClient
}

func NewAuthHandler(cfg config.GRPCServiceConfig) (*AuthHandler, error) {
	client, err := NewGRPCClient(cfg)
	if err != nil {
		return nil, err
	}

	return &AuthHandler{grpcClient: client}, nil
}

func (h *AuthHandler) Close() error {
	return h.grpcClient.Close()
}

func (h * AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}

	var req *auth_grpc.LoginRequest

	if err := json.NewDecoder(r.Body).Decode(req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
	}

	resp, err := h.grpcClient.Login(r.Context(), req)
	if err != nil {
		http.Error(w, "Authentication failed", http.StatusUnauthorized)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
