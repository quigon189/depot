package handlers

import (
	"dep-go-catalog/internal/services"
	"encoding/json"
	"net/http"
	"strconv"
)

type BaseHandler struct {
	Service services.Service
}

func (h *BaseHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch r.Method {
	case http.MethodPost:
		h.createBatch(w, r)
	case http.MethodGet:
		path := r.PathValue("id")
		switch path {
		case "all":
			h.getAll(w, r)
		default:
			h.get(w, r)
		}
	case http.MethodPut:
		h.put(w, r)
	case http.MethodDelete:
		h.delete(w,r)
	default:
		handleError(w, ErrMetodNotAllowed)
	}
}

func (h *BaseHandler) createBatch(w http.ResponseWriter, r *http.Request) {
	m := h.Service.NewModels()

	if err := json.NewDecoder(r.Body).Decode(m); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.Create(r.Context(), m); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusCreated, m)
}

func (h *BaseHandler) get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	m := h.Service.NewModel()

	if err := h.Service.Get(r.Context(), m, uint(id)); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &m)
}

func (h *BaseHandler) getAll(w http.ResponseWriter, r *http.Request) {
	m := h.Service.NewModels()
	if err := h.Service.GetAll(r.Context(), m); err != nil {
		handleError(w, err)
		return
	}
	encode(w, http.StatusOK, m)
}

func (h *BaseHandler) put(w http.ResponseWriter, r *http.Request) {
	m := h.Service.NewModel()

	if err := json.NewDecoder(r.Body).Decode(m); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.Update(r.Context(), m); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, m)
}

func (h *BaseHandler) delete(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	m := h.Service.NewModel()

	if err := h.Service.Get(r.Context(), m, uint(id)); err != nil {
		handleError(w, err)
		return
	}

	if err := h.Service.Delete(r.Context(), m); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, m)
}
