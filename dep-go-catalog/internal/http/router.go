package http

import (
	"dep-go-catalog/internal/handlers"
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewRouter(
	specService *services.SpecService,
	groupService *services.GroupService,
) http.Handler {
	mux := http.NewServeMux()

	specHandler := &handlers.SpecHandler{Service: specService}
	groupHandler := &handlers.GroupHandler{Service: groupService}

	mux.Handle("GET /specialties/{id}", specHandler)
	mux.Handle("POST /specialties", specHandler)

	mux.Handle("POST /groups", groupHandler)
	mux.Handle("GET /groups/{id}", groupHandler)

	return mux
}
