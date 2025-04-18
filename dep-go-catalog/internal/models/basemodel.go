package models

import (
	"time"
)

type BaseModel struct {
	ID        uint      `gorm:"primaryKey"`
	CreatedAt time.Time `gorm:"autoCreateTime"`
	DeletedAt time.Time
}
