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
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
	}
}

func (h *SpecHandler) createSpec(w http.ResponseWriter, r *http.Request) {
	var spec models.Specialty

	if err := json.NewDecoder(r.Body).Decode(&spec); err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	if err := h.Service.CreateSpec(r.Context(), &spec); err != nil {
		//исправить тут временная заглушка
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}

	//	spec.Groups = []models.Group{}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(&spec)
}

func (h *SpecHandler) getSpec(w http.ResponseWriter, r *http.Request) {
	sid := r.PathValue("id")

	id, err := strconv.ParseUint(sid, 10, 0)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	spec, err := h.Service.GetWithGroup(r.Context(), uint(id))
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(spec)
}
