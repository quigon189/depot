package server

import (
	"auth-service/internal/config"
	"auth-service/internal/service"

	"google.golang.org/grpc"
)

type GRPCServer struct {
	config      *config.Config
	authService *service.AuthService
	server      *grpc.Server
}

func NewGRPCServer(cfg *config.Config, authService *service.AuthService) *GRPCServer {
	return &GRPCServer{
		config:      cfg,
		authService: authService,
		server:      grpc.NewServer(),
	}
}
