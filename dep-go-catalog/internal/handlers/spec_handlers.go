package handlers

import (
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewSpecHandler(service services.Service) http.Handler {
	var handler BaseHandler
	handler.Service = service

	return &handler
}

// type SpecHandler struct {
// 	Service *services.SpecService
// }

// func (h *SpecHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
// 	switch r.Method {
// 	case http.MethodPost:
// 		h.create(w, r)
// 	case http.MethodGet:
// 		path := r.PathValue("id")
// 		switch path {
// 		case "all":
// 			h.getAll(w, r)
// 		default:
// 			h.get(w, r)
// 		}
// 	default:
// 		handleError(w, ErrMetodNotAllowed)
// 	}
// }
//
// func (h *SpecHandler) create(w http.ResponseWriter, r *http.Request) {
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
//
// func (h *SpecHandler) get(w http.ResponseWriter, r *http.Request) {
// 	id, err := strconv.ParseUint(r.PathValue("id"), 10, 0)
// 	if err != nil {
// 		handleError(w, ErrInvalidData)
// 		return
// 	}
//
// 	spec := h.Service.NewModel()
//
// 	 if err := h.Service.Get(r.Context(), spec, uint(id)); err != nil {
// 		handleError(w, err)
// 		return
// 	}
//
// 	encode(w, http.StatusOK, &spec)
// }
//
// func (h *SpecHandler) getAll(w http.ResponseWriter, r *http.Request) {
// 	specs := h.Service.NewModels()
// 	if err := h.Service.GetAll(r.Context(), specs); err != nil {
// 		handleError(w, err)
// 		return
// 	}
// 	encode(w, http.StatusOK, specs)
// }
