package handlers

import (
	"dep-go-catalog/internal/models"
	"dep-go-catalog/internal/services"
	"encoding/json"
	"net/http"
	"strconv"
)

type SpecHandler struct {
	Service *services.SpecService
}

func (h *SpecHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		h.createSpec(w, r)
	case http.MethodGet:
		h.getSpec(w, r)
	default:
		handleError(w, ErrMetodNotAllowed)
	}
}

func (h *SpecHandler) createSpec(w http.ResponseWriter, r *http.Request) {
	var spec models.Specialty

	//	w.Header().Set("Content-Type", "application/json")

	if err := json.NewDecoder(r.Body).Decode(&spec); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.CreateSpec(r.Context(), &spec); err != nil {
		handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(&spec)
}

func (h *SpecHandler) getSpec(w http.ResponseWriter, r *http.Request) {
	sid := r.PathValue("id")

	//	w.Header().Set("Content-Type", "application/json")

	id, err := strconv.ParseUint(sid, 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	spec, err := h.Service.GetWithGroup(r.Context(), uint(id))
	if err != nil {
		handleError(w, err)
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(spec)
}
