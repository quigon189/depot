package services

import (
	"context"
	"errors"
	"reflect"

	"gorm.io/gorm"
)

type Service interface {
	NewModel() ServiceModel
	NewModels() ServiceModel

	Create(ctx context.Context, model ServiceModel) error
	Get(ctx context.Context, model any, id uint) error
	GetAll(ctx context.Context, models any) error
}

type ServiceModel interface {
	Validate() error
}

var (
	ErrNotFound     = errors.New("record not found")
	ErrInvalidInput = errors.New("invalid input data")
	ErrConflict     = errors.New("data confilct")
)

type BaseService struct {
	db       *gorm.DB
	preloads []string
}

func NewBaseService(db *gorm.DB) *BaseService {
	return &BaseService{db: db}
}

func (s *BaseService) Create(ctx context.Context, model ServiceModel) error {
	if err := model.Validate(); err != nil {
		return err
	}

	return s.db.WithContext(ctx).Create(model).Error
}

func (s *BaseService) Get(ctx context.Context, model any, id uint) error {
	tx := s.db.WithContext(ctx)
	for _, p := range s.preloads {
		tx = tx.Preload(p)
	}
	switch tx.First(model, "id = ?", id).Error {
	case gorm.ErrRecordNotFound:
		return ErrNotFound
	default:
		return nil
	}

}

func (s *BaseService) GetAll(ctx context.Context, models any) error {
	t := reflect.TypeOf(models)
	if t.Kind() != reflect.Pointer {
		return errors.New("model type is not pointer")
	}
	tx := s.db.WithContext(ctx)
	for _, p := range s.preloads {
		tx = tx.Preload(p)
	}
	return tx.Find(models).Error
}
