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
		h.create(w, r)
	case http.MethodGet:
		path := r.PathValue("id")
		switch path {
		case "all":
			h.getAll(w, r)
		default:
			h.get(w, r)
		}
	default:
		handleError(w, ErrMetodNotAllowed)
	}
}

func (h *SpecHandler) create(w http.ResponseWriter, r *http.Request) {
	var spec models.Specialty

	if err := json.NewDecoder(r.Body).Decode(&spec); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.CreateSpec(r.Context(), &spec); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusCreated, &spec)
}

func (h *SpecHandler) get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	spec, err := h.Service.GetWithGroup(r.Context(), uint(id))
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &spec)
}

func (h *SpecHandler) getAll(w http.ResponseWriter, r *http.Request) {
	specs, err := h.Service.GetAll(r.Context())
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &specs)
}
