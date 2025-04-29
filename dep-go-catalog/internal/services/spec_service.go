package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type specialty struct {
	models.Specialty
}

func (m specialty) Validate() error {
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
	service := &SpecService{
		BaseService: NewBaseService(db),
	}

	service.preloads = []string{"Groups", "Groups.Teacher", "Groups.Students"}

	return service
}

func (s *SpecService) NewModel() *specialty {
	return &specialty{}
}

func (s *SpecService) NewModels() *[]specialty {
	specs := make([]specialty, 0)
	return &specs
}
