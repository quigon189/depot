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

func NewSpecService(db *gorm.DB) *SpecService {
	return &SpecService{
		BaseService: NewBaseService(db),
	}
}

func (s *SpecService) CreateSpec(ctx context.Context, spec *models.Specialty) error {
	if len(spec.Code) != 8 || spec.Code[2] != '.' || spec.Code[5] != '.' {
		return ErrInvalidInput
	}

	if spec.Name == "" || len(spec.Name) > 100 {
		return ErrInvalidInput
	}

	if spec.ShortName == "" || len(spec.ShortName) > 3 {
		return ErrInvalidInput
	}

	return s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
		var existing models.Specialty
		if err := tx.Where("code = ?", spec.Code).First(&existing).Error; err == nil {
			return ErrConflict
		}
		return tx.Create(spec).Error
	})
}

func (s *SpecService) GetWithGroup(ctx context.Context, id uint) (*models.Specialty, error) {
	var spec models.Specialty
	err := s.db.WithContext(ctx).
		Preload("Groups").
		Preload("Groups.Teacher").
		First(&spec, "id = ?", id).Error
		
	if errors.Is(err, gorm.ErrRecordNotFound) {
		return nil, ErrNotFound
	}

	return &spec, nil
}
