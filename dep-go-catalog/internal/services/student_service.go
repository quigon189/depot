package services

import (
	"context"
	"dep-go-catalog/internal/models"
	"errors"

	"gorm.io/gorm"
)

type StudentService struct {
	*BaseService
}

func NewStudentService(db *gorm.DB) *StudentService {
	return &StudentService{
		BaseService: NewBaseService(db),
	}
}

func (s *StudentService) CreateStudent(ctx context.Context, student *models.Student) error {
	if student.FirstName == "" ||
		student.MiddleName == "" ||
		student.LastName == "" ||
		student.BirthDate == "" {
		return ErrInvalidInput
	}

	return s.db.WithContext(ctx).Create(student).Error
}

func (s *StudentService) GetStudent(ctx context.Context, id uint) (*models.Student, error) {
	var student models.Student

	err := s.db.WithContext(ctx).Preload("Group").First(&student).Error
	switch {
	case errors.Is(err, gorm.ErrRecordNotFound):
		return nil, ErrNotFound
	case err != nil:
		return nil, err
	}

	return &student, nil
}

func (s *StudentService) GetAllStudent(ctx context.Context) ([]models.Student, error) {
	var students []models.Student

	if err := s.db.WithContext(ctx).Find(&students).Error; err != nil {
		return nil, err
	}

	return students, nil
}
