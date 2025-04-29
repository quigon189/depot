package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type classroom struct {
	models.Classroom
}

func (m *classroom) Validate() error {
	switch {
	case m.Number == 0:
		return ErrInvalidInput
	case m.Name == "":
		return ErrInvalidInput
	case m.Type == "":
		return ErrInvalidInput
	case m.TeacherID == 0:
		return ErrInvalidInput
	default:
		return nil
	}
}

type classes []classroom

func (m *classes) Validate() error {
	return nil
}

type ClassService struct {
	*BaseService
}

func NewClassService(db *gorm.DB) *ClassService {
	service := &ClassService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Teacher", "Disciplines"}

	return service
}

func (s *ClassService) NewModel() ServiceModel {
	return &classroom{}
}

func (s *ClassService) NewModels() ServiceModel {
	return &classes{}
}
