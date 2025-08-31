package service

import (
	"auth-service/internal/database"
	"time"
)

type AuthService struct {
	db *database.PostgresDB
	jwtSecret string
	tokenExpiry time.Duration
}
