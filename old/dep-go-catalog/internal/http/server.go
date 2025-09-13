package http

import (
	"dep-go-catalog/internal/services"
	"net/http"

	"gorm.io/gorm"
)

type Server struct {
	addr   string
	router http.Handler
}

func NewServer(db *gorm.DB, addr string) *Server {
	var srv Server

	specService := services.NewSpecService(db)
	teacherService := services.NewTeacherService(db)
	groupService := services.NewGroupService(db)
	studentService := services.NewStudentService(db)
	disciplineService := services.NewDisciplineService(db)
	classService := services.NewClassService(db)

	srv.router = NewRouter(
		specService,
		groupService,
		teacherService,
		studentService,
		disciplineService,
		classService,
	)

	srv.addr = addr

	return &srv
}

func (s *Server) Serve() error {
	return http.ListenAndServe(s.addr, loggingMiddlware(s.router))
}
