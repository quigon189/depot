package handlers

import (
	"dep-go-catalog/internal/services"
/* 	"net/http" */
)

type StudentHandler struct {
	Service services.StudentService
}

// func (h *StudentHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
// 	switch r.Method {
// 	case http.MethodPost:
// 		h.create(w, r)
// 	case http.MethodGet:
// 		h.get(w, r)
// 	}
// }
