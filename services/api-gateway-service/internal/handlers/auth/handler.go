package auth

import (
	"api-gateway-service/internal/config"
	"api-gateway-service/internal/grpc/auth_grpc"
	"api-gateway-service/internal/handlers/submux"
	"encoding/json"
	"log"
	"net/http"
)

func SetupAuth(cfg config.GRPCServiceConfig, mux *submux.SubMux) error {
	authHandler, err := NewAuthHandler(cfg)
	mux.HandleFunc("/login", authHandler.Login)
	mux.HandleFunc("/register", authHandler.Register)
	return err
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

func (h *AuthHandler) Login(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req auth_grpc.LoginRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		return
	}

	resp, err := h.grpcClient.Login(r.Context(), &req)
	if err != nil {
		http.Error(w, "Authentication failed", http.StatusUnauthorized)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}

func (h *AuthHandler) Register(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req auth_grpc.RegisterRequest

	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid JSON", http.StatusBadRequest)
		log.Printf("Invalid JSON: %v error: %v", &req, err)
		return
	}

	resp, err := h.grpcClient.Register(r.Context(), &req)
	if err != nil {
		http.Error(w, "Registration failed", http.StatusUnauthorized)
		log.Printf("Registration failed response: %v error: %s", resp, err.Error())
		return
	}

	log.Printf("created user: %v", resp)
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)

}
