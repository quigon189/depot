package handlers

import (
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewDisciplineHandler(service services.Service) http.Handler {
	return &BaseHandler{Service: service}
}
