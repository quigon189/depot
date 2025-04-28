package handlers

import (
	"dep-go-catalog/internal/models"
	"dep-go-catalog/internal/services"
	"encoding/json"
	"net/http"
	"strconv"
)

type TeacherHandler struct {
	Service *services.TeacherService
}

func (h *TeacherHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		h.create(w,r)
	case http.MethodGet:
		h.get(w, r)
	default:
		handleError(w, ErrMetodNotAllowed)
	}
}

func (h *TeacherHandler) create(w http.ResponseWriter, r *http.Request) {
	var teacher models.Teacher

	if err := json.NewDecoder(r.Body).Decode(&teacher); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.CreateTeacher(r.Context(), &teacher); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusCreated, &teacher)
}

func (h *TeacherHandler) get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, err) 
		return
	}

	teacher, err := h.Service.GetTeacher(r.Context(), uint(id))
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &teacher)
}

func (h *TeacherHandler) getAll(w http.ResponseWriter, r *http.Request) {
	teachers, err := h.Service.GetAllTeacher(r.Context())
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &teachers)
}
