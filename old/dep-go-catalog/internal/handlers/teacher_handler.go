package handlers

import (
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewTeacherHandler(service services.Service) http.Handler {
	return &BaseHandler{Service: service}
}
