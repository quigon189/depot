package services

import (
	"context"
	"dep-go-catalog/internal/models"
	"errors"

	"gorm.io/gorm"
)

type SpecService struct {
	*BaseService
}

type specialty struct {
	*models.Specialty
}

func (m *specialty) Validate() error {
	return nil
}

func NewSpecService(db *gorm.DB) *SpecService {
	service := &SpecService{
		BaseService: NewBaseService(db),
	}

	service.preloads = []string{"Groups", "Groups.Teacher"}

	return service
}

func (s *SpecService) NewSpecModel() *specialty {
	return &specialty{}
}

func (s *SpecService) NewSpecModels() []specialty {
	return []specialty{}
}

// func (s *SpecService) CreateSpec(ctx context.Context, spec *models.Specialty) error {
// 	if len(spec.Code) != 8 || spec.Code[2] != '.' || spec.Code[5] != '.' {
// 		return ErrInvalidInput
// 	}
//
// 	if spec.Name == "" || len(spec.Name) > 100 {
// 		return ErrInvalidInput
// 	}
//
// 	if spec.ShortName == "" || len(spec.ShortName) > 3 {
// 		return ErrInvalidInput
// 	}
//
// 	return s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
// 		var existing models.Specialty
// 		if err := tx.Where("code = ?", spec.Code).First(&existing).Error; err == nil {
// 			return ErrConflict
// 		}
// 		return tx.Create(spec).Error
// 	})
// }

// func (s *SpecService) Get(ctx context.Context, id uint) (*models.Specialty, error) {
// 	var spec models.Specialty
//
// 	err := s.db.WithContext(ctx).First(&spec, "id = ?", id).Error
// 	switch {
// 	case errors.Is(err, gorm.ErrRecordNotFound):
// 		return nil, ErrNotFound
// 	case err != nil:
// 		return nil, err
// 	}
//
// 	return &spec, nil
// }
//
// func (s *SpecService) GetWithGroup(ctx context.Context, id uint) (*models.Specialty, error) {
// 	var spec models.Specialty
// 	err := s.db.WithContext(ctx).
// 		Preload("Groups").
// 		Preload("Groups.Teacher").
// 		First(&spec, "id = ?", id).Error
// 	switch {
// 	case errors.Is(err, gorm.ErrRecordNotFound):
// 		return nil, ErrNotFound
// 	case err != nil:
// 		return nil, err
// 	}
//
// 	return &spec, nil
// }
//
// func (s *SpecService) GetAll(ctx context.Context) ([]models.Specialty, error) {
// 	var specs []models.Specialty
// 	err := s.db.WithContext(ctx).
// 		Preload("Groups").
// 		Preload("Groups.Teacher").
// 		Find(&specs).Error
// 	if errors.Is(err, gorm.ErrRecordNotFound) {
// 		return nil, ErrNotFound
// 	}
// 	if err != nil {
// 		return nil, err
// 	}
//
// 	return specs, nil
// }
