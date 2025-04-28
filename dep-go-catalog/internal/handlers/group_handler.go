package handlers

import (
	"dep-go-catalog/internal/models"
	"dep-go-catalog/internal/services"
	"encoding/json"
	"net/http"
	"strconv"
)

type GroupHandler struct {
	Service *services.GroupService
}

func (h *GroupHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
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

func (h *GroupHandler) create(w http.ResponseWriter, r *http.Request) {
	var group models.Group

	if err := json.NewDecoder(r.Body).Decode(&group); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.CreateGroup(r.Context(), &group); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusCreated, &group)
}

func (h *GroupHandler) get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	group, err := h.Service.GetGroup(r.Context(), uint(id))
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &group)
}

func (h *GroupHandler) getAll(w http.ResponseWriter, r *http.Request) {
	var groups []models.Group

	groups, err := h.Service.GetAllGroup(r.Context())
	if err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &groups)
}
