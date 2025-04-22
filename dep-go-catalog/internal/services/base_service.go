package services

import (
	"errors"

	"gorm.io/gorm"
)

var (
	ErrNotFound     = errors.New("record not found")
	ErrInvalidInput = errors.New("invalid input data")
	ErrConflict     = errors.New("data confilct")
)

type BaseService struct {
	db *gorm.DB
}

func NewBaseService(db *gorm.DB) *BaseService {
	return &BaseService{db: db}
}
