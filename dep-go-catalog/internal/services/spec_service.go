package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type specialty struct {
	models.Specialty
}

type specialties []specialty

func (m *specialties) Validate() error {
	for _,s := range *m {
		if err := s.Validate(); err != nil {
			return err
		}
	}
	return nil
}

func (m *specialty) Validate() error {
	if len(m.Code) != 8 || m.Code[2] != '.' || m.Code[5] != '.' {
		return ErrInvalidInput
	}

	if m.Name == "" || len(m.Name) > 200 {
		return ErrInvalidInput
	}

	if m.ShortName == "" || len(m.ShortName) > 8 {
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
	return &specialty{}
}

func (s *SpecService) NewModels() ServiceModel {
	return &specialties{}
}
