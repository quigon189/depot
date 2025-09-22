package server

import (
	"net/http"
	"render-service/internal/handlers"
)

func (s *Server) setupRouter() {
	mux := http.NewServeMux()

	handlers := handlers.New(s.templates)

	mux.HandleFunc("/", handlers.Index)
	mux.HandleFunc("/404", handlers.NotFound)

	fs := http.FileServer(http.Dir("./static"))
	mux.Handle("/static/", http.StripPrefix("/static/", fs))

	mux.Handle("/health", http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	}))

	s.httpServer.Handler = mux
}
