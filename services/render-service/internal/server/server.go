package server

import (
	"context"
	"html/template"
	"log"
	"net/http"
	"render-service/internal/config"
	"strconv"
)

type Server struct {
	httpServer *http.Server
	config     *config.Config
	templates  *template.Template
}

func NewServer(cfg *config.Config) *Server {

	return &Server{
		httpServer: &http.Server{
			Addr:         cfg.Server.Address + ":" + strconv.Itoa(cfg.Server.Port),
			ReadTimeout:  cfg.Server.ReadTimeout,
			WriteTimeout: cfg.Server.WriteTimeout,
			IdleTimeout:  cfg.Server.IdleTimeout,
		},
		config: cfg,
	}
}

func (s *Server) Start() error {
	s.setupRouter()

	log.Printf("Starting API Gateway on address %s:%d", s.config.Server.Address, s.config.Server.Port)
	return s.httpServer.ListenAndServe()
}

func (s *Server) Shutdown(ctx context.Context) error {
	return s.httpServer.Shutdown(ctx)
}
