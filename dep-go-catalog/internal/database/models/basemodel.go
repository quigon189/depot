package models

import "time"

type BaseModel struct {
	ID        uint
	CreatedAt time.Time
	DeletedAt time.Time
}
