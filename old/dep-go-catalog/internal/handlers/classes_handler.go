package handlers

import (
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewClassHandler(service services.Service) http.Handler {
	return &BaseHandler{Service: service}
}
