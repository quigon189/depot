package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type specialtyModel struct {
	models.Specialty
}

type specialties []specialtyModel

func (m *specialties) Validate() error {
	return nil
}

func (m *specialtyModel) Validate() error {
	if len(m.Code) != 8 || m.Code[2] != '.' || m.Code[5] != '.' {
		return ErrInvalidInput
	}

	if m.Name == "" || len(m.Name) > 100 {
		return ErrInvalidInput
	}

	if m.ShortName == "" || len(m.ShortName) > 3 {
		return ErrInvalidInput
	}
	return nil
}

type SpecService struct {
	*BaseService
}

func NewSpecService(db *gorm.DB) *SpecService {
	service := &SpecService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Groups", "Groups.Teacher", "Groups.Students"}

	return service
}

func (s *SpecService) NewModel() ServiceModel {
	return &specialtyModel{}
}

func (s *SpecService) NewModels() ServiceModel {
	return &specialties{}
}
