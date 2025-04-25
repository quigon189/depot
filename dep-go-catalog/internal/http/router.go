package http

import (
	"dep-go-catalog/internal/handlers"
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewRouter(
	specService *services.SpecService,
) http.Handler {
	mux := http.NewServeMux()

	specHandler := &handlers.SpecHandler{Service: specService}

	mux.Handle("GET /specialties/{id}", specHandler)
	mux.Handle("POST /specialties", specHandler)

	return mux
}
