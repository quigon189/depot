package server

import (
	"auth-service/internal/config"
	"auth-service/internal/grpc/auth_grpc"
	"auth-service/internal/service"
	"log"
	"net"

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

func (s *GRPCServer) Start() error {
	lis, err := net.Listen("tcp",s.config.Server.Address+":"+s.config.Server.GRPCPort)
	if err != nil {
		return err
	}

	auth_grpc.RegisterAuthServiceServer(s.server, s.authService)
	
	log.Printf("Starting gRPC server on &s:&s", s.config.Server.Address, s.config.Server.GRPCPort)
	return s.server.Serve(lis)
}

func (s *GRPCServer) Stop() {
	s.server.GracefulStop()
}
