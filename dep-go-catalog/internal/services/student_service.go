package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type student struct {
	models.Student
}

func (m *student) Validate() error {
	switch {
	case m.FirstName == "":
		return ErrInvalidInput
	case m.MiddleName == "":
		return ErrInvalidInput
	case m.LastName == "":
		return ErrInvalidInput
	case m.GroupID == 0:
		return ErrInvalidInput
	case m.BirthDate == "":
		return ErrInvalidInput
	default:
		return nil
	}
}

type students []student

func (m *students) Validate() error {
	return nil
}

type StudentService struct {
	*BaseService
}

func NewStudentService(db *gorm.DB) *StudentService {
	service := &StudentService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Group"}
	return service
}

func (s *StudentService) NewModel() ServiceModel {
	return &student{}
}

func (s *StudentService) NewModels() ServiceModel {
	return &students{}
}
