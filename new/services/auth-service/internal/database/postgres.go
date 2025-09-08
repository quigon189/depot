package database

import (
	"auth-service/internal/config"
	"database/sql"
	"fmt"
)

type PostgresDB struct {
	db *sql.DB
}

func NewPostresDB(cfg *config.DBConfig) (*PostgresDB, error) {
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.Name)
}
