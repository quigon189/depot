package server

import (
	"api-gateway-service/internal/config"
	"context"
	"log"
	"net/http"
	"strconv"
)

type Server struct {
	httpServer *http.Server
	config     *config.Config
}

func NewServer(cfg *config.Config) *Server {
	router := setupRouter()

	return &Server{
		httpServer: &http.Server{
			Addr:         cfg.Server.Address + ":" + strconv.Itoa(cfg.Server.Port),
			Handler:      router,
			ReadTimeout:  cfg.Server.ReadTimeout,
			WriteTimeout: cfg.Server.WriteTimeout,
			IdleTimeout:  cfg.Server.IdleTimeout,
		},
		config: cfg,
	}
}

func (s *Server) Start() error {
	log.Printf("Starting API Gateway on address %s:%d", s.config.Server.Address, s.config.Server.Port)
	return s.httpServer.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	return s.httpServer.Shutdown(ctx)
}
