package services

import (
	"context"
	"dep-go-catalog/internal/models"
	"errors"

	"gorm.io/gorm"
)

type GroupService struct {
	*BaseService
	specService *SpecService
}

func NewGroupService(
	db *gorm.DB,
	specService *SpecService,
) *GroupService {
	return &GroupService{
		BaseService: NewBaseService(db),
		specService: specService,
	}
}

func (s *GroupService) CreateGroup(ctx context.Context, group *models.Group) error {
	if group.Number == 0 || group.YearFormed == 0 || group.SpecID == 0 {
		return ErrInvalidInput
	}
	if _, err := s.specService.Get(ctx, group.SpecID); err != nil {
		switch err {
		case ErrNotFound:
			return ErrInvalidInput
		default:
			return err
		}
	}

	// Добавить проверку сеществования преподавателя

	return s.db.WithContext(ctx).Create(&group).Error
}

func (s *GroupService) GetGroup(ctx context.Context, id uint) (*models.Group, error) {
	var group models.Group

	err := s.db.WithContext(ctx).
		Preload("Students").
		Preload("Disciplines").
		Preload("Teacher").
		First(&group, "id = ?", id).Error

	switch {
	case errors.Is(err, gorm.ErrRecordNotFound):
		return nil, ErrNotFound
	case err != nil:
		return nil, err
	}

	return &group, nil
}

func (s *GroupService) GetAllGroup(ctx context.Context) ([]models.Group, error) {
	var groups []models.Group

	err := s.db.WithContext(ctx).
		Preload("Students").
		Preload("Disciplines").
		Preload("Teacher").
		Find(&groups).Error

	if err != nil {
		return nil, err
	}

	return groups, nil
}
