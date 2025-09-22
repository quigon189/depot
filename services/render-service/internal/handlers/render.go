package handlers

import (
	"html/template"
	"net/http"
	"render-service/views"
)

type Handler struct {
	templates *template.Template
}

func New(templates *template.Template) *Handler {
	return &Handler{
		templates: templates,
	}
}

func (h *Handler) Index(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path != "/" {
		h.NotFound(w,r)
		return
	}

	views.Index().Render(r.Context(), w)
}

func (h *Handler) NotFound(w http.ResponseWriter, r *http.Request) {
	w.WriteHeader(http.StatusNotFound)
	views.NotFound().Render(r.Context(), w)
}
