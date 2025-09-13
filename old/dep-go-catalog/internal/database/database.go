package database

import (
	"dep-go-catalog/internal/config"
	"dep-go-catalog/internal/models"
	"fmt"

	"gorm.io/driver/postgres"
	"gorm.io/gorm"
)

func Connect(cfg *config.Config) *gorm.DB {
	dsn := fmt.Sprintf(
		"host=%s user=%s password=%s dbname=%s port=%s sslmode=disable",
		cfg.DB.Host,
		cfg.DB.User,
		cfg.DB.Pass,
		cfg.DB.Name,
		cfg.DB.Port,
	)
	db, err := gorm.Open(postgres.Open(dsn), &gorm.Config{})
	if err != nil {
		panic("Failed to connect to database!")
	}
	return db
}

func AutoMigrate(db *gorm.DB) error {
	return db.AutoMigrate(
		&models.Specialty{},
		&models.Group{},
		&models.Student{},
		&models.Teacher{},
		&models.Discipline{},
		&models.Classroom{},
	)
}
