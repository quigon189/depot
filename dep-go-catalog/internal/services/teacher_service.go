package services

import (
	"context"
	"dep-go-catalog/internal/models"
	"errors"

	"gorm.io/gorm"
)

type TeacherService struct {
	*BaseService
}

func NewTeacherService(db *gorm.DB) *TeacherService {
	return &TeacherService{
		BaseService: NewBaseService(db),
	}
}

func (s *TeacherService) CreateTeacher(ctx context.Context, teacher *models.Teacher) error {
	if teacher.FirstName == "" ||
		teacher.MiddleName == "" ||
		teacher.LastName == "" {
		return ErrInvalidInput	
	}

	return s.db.WithContext(ctx).Create(&teacher).Error
}

func (s *TeacherService) GetTeacher(ctx context.Context, id uint) (*models.Teacher, error) {
	var teacher models.Teacher

	err := s.db.WithContext(ctx).First(&teacher, "id = ?", id).Error
	switch {
	case errors.Is(err, gorm.ErrRecordNotFound):
		return nil, ErrNotFound
	case err != nil:
		return nil, err
	}

	return &teacher, nil
}

func (s *TeacherService) GetAllTeacher(ctx context.Context) ([]models.Teacher, error) {
	var teachers []models.Teacher

	err := s.db.WithContext(ctx).Find(&teachers).Error
	if err != nil {
		return nil, err
	}

	return teachers, nil

}
