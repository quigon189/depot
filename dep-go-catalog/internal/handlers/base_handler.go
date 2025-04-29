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
	default:
		handleError(w, ErrMetodNotAllowed)
	}
}

// func (h *BaseHandler) create(w http.ResponseWriter, r *http.Request) {
// 	spec := h.Service.NewModel()
//
// 	if err := json.NewDecoder(r.Body).Decode(spec); err != nil {
// 		handleError(w, ErrInvalidData)
// 		return
// 	}
//
// 	if err := h.Service.Create(r.Context(), spec); err != nil {
// 		handleError(w, err)
// 		return
// 	}
//
// 	encode(w, http.StatusCreated, spec)
// }

func (h *BaseHandler) createBatch(w http.ResponseWriter, r *http.Request) {
	spec := h.Service.NewModels()

	if err := json.NewDecoder(r.Body).Decode(spec); err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	if err := h.Service.Create(r.Context(), spec); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusCreated, spec)
}

func (h *BaseHandler) get(w http.ResponseWriter, r *http.Request) {
	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
	if err != nil {
		handleError(w, ErrInvalidData)
		return
	}

	spec := h.Service.NewModel()

	if err := h.Service.Get(r.Context(), spec, uint(id)); err != nil {
		handleError(w, err)
		return
	}

	encode(w, http.StatusOK, &spec)
}

func (h *BaseHandler) getAll(w http.ResponseWriter, r *http.Request) {
	specs := h.Service.NewModels()
	if err := h.Service.GetAll(r.Context(), specs); err != nil {
		handleError(w, err)
		return
	}
	encode(w, http.StatusOK, specs)
}
