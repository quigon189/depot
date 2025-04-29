package handlers

import (
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewGroupHandler(service services.Service) http.Handler {
	return &BaseHandler{Service: service} 
}
