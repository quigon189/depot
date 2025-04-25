package models

import (
	"time"
)

type BaseModel struct {
	ID        uint      `gorm:"primaryKey" json:"id"` 
	CreatedAt time.Time `gorm:"autoCreateTime" json:"-"`
	DeletedAt time.Time `json:"-"`
}
