package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type teacher struct {
	models.Teacher
}

func (m *teacher) Validate() error {
	switch {
	case m.FirstName == "":
		return ErrInvalidInput
	case m.MiddleName == "":
		return ErrInvalidInput
	case m.LastName == "":
		return ErrInvalidInput
	default:
		return nil
	}
}

type teachers []teacher

func (m *teachers) Validate() error {
	return nil
}

type TeacherService struct {
	*BaseService
}

func NewTeacherService(db *gorm.DB) *TeacherService {
	service := &TeacherService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Groups", "Disciplines"}
	return service
}

func (s *TeacherService) NewModel() ServiceModel {
	return &teacher{}
}

func (s *TeacherService) NewModels() ServiceModel {
	return &teachers{}
}
