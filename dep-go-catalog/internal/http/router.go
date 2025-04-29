package http

import (
	"dep-go-catalog/internal/handlers"
	"dep-go-catalog/internal/services"
	"net/http"
)

func NewRouter(
	specService *services.SpecService,
	groupService *services.GroupService,
	teacherService *services.TeacherService,
) http.Handler {
	mux := http.NewServeMux()

	specHandler := handlers.NewSpecHandler(specService) 
	groupHandler := handlers.NewGroupHandler(groupService)
	teacherHandler := &handlers.TeacherHandler{Service: teacherService}

	mux.Handle("GET /specialties/{id}", specHandler)
	mux.Handle("POST /specialties", specHandler)

	mux.Handle("GET /groups/{id}", groupHandler)
	mux.Handle("POST /groups", groupHandler)

	mux.Handle("GET /teachers/{id}", teacherHandler)
	mux.Handle("POST /teachers", teacherHandler)

	return mux
}
