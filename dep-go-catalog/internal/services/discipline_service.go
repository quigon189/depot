package services

import (
	"dep-go-catalog/internal/models"

	"gorm.io/gorm"
)

type discipline struct {
	models.Discipline
}

func (m *discipline) Validate() error {
	switch {
	case m.Code == "":
		return ErrInvalidInput
	case m.Name == "":
		return ErrInvalidInput
	case m.Semester == 0:
		return ErrInvalidInput
	case m.Hours == 0:
		return ErrInvalidInput
	case m.GroupID == 0:
		return ErrInvalidInput
	default:
		return nil
	}
}

type disciplines []discipline

func (m *disciplines) Validate() error {
	return nil
}

type DisciplineService struct {
	*BaseService
}

func NewDisciplineService(db *gorm.DB) *DisciplineService {
	service := &DisciplineService{BaseService: NewBaseService(db)}
	service.preloads = []string{"Group", "Group.Specialty", "Classes", "Teachers"}
	return service
}

func (s *DisciplineService) NewModel() ServiceModel {
	return &discipline{}
}

func (s *DisciplineService) NewModels() ServiceModel {
	return &disciplines{}
}
