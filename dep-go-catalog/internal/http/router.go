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
	studentService *services.StudentService,
	disciplineService *services.DisciplineService,
	classService *services.ClassService,
) http.Handler {
	mux := http.NewServeMux()

	specHandler := handlers.NewSpecHandler(specService) 
	groupHandler := handlers.NewGroupHandler(groupService)
	teacherHandler := handlers.NewTeacherHandler(teacherService)
	studentHandler := handlers.NewStudentHandler(studentService)
	disciplineHandler := handlers.NewDisciplineHandler(disciplineService)
	classHandler := handlers.NewClassHandler(classService)

	mux.Handle("GET /specialties/{id}", specHandler)
	mux.Handle("POST /specialties", specHandler)

	mux.Handle("GET /groups/{id}", groupHandler)
	mux.Handle("POST /groups", groupHandler)

	mux.Handle("GET /teachers/{id}", teacherHandler)
	mux.Handle("POST /teachers", teacherHandler)

	mux.Handle("GET /students/{id}", studentHandler)
	mux.Handle("POST /students", studentHandler)

	mux.Handle("GET /disciplines/{id}", disciplineHandler)
	mux.Handle("POST /disciplines", disciplineHandler)

	mux.Handle("GET /classes/{id}", classHandler)
	mux.Handle("POST /classes", classHandler)

	return mux
}
