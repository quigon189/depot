package database

import (
	"auth-service/internal/config"
	"context"
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/lib/pq"
	"github.com/pelletier/go-toml/query"
	"github.com/pressly/goose/v3"
)

type PostgresDB struct {
	db *sql.DB
}

func NewPostresDB(cfg *config.DBConfig) (*PostgresDB, error) {
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s",
		cfg.Host, cfg.Port, cfg.User, cfg.Password, cfg.Name)

	db, err := sql.Open("postgres", connStr)
	if err != nil {
		return nil, err
	}

	// различные ограничения
	db.SetMaxOpenConns(8)
	db.SetMaxIdleConns(4)
	db.SetConnMaxLifetime(5 * time.Minute)

	//проверяем соединение
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := db.PingContext(ctx); err != nil {
		return nil, err
	}

	if err := goose.Up(db, cfg.MigrationsPath); err != nil {
		return nil, fmt.Errorf("failed to apply migrations: %v", err)
	}

	log.Println("Database connected and migrations applied successfully")

	return &PostgresDB{db: db}, nil
}

func (p *PostgresDB) Close() error {
	return p.db.Close()
}

func (p *PostgresDB) GetUserByLogin(login string) (*User, error) {
	query := `
		SELECT id, email, password_hash, is_active,
			is_verified, created_at, updated_at, last_login_at
		FROM users
		WHERE email = $1 OR username = $1
	`

	user := &User{}
	err := p.db.QueryRow(query, login).Scan(
		&user.ID, &user.Email, &user.PasswordHash, &user.IsActive,
		&user.IsVerified, &user.CreatedAt, &user.UpdatedAt, &user.LastLoginAt,
	)

	if err != nil {
		return nil, err
	}

	return user, nil
}

func (p *PostgresDB) UpdateLastLogin(id int64) error {
	query := `
	UPDATE users SET last_login_at = NOW() WHERE id = $1
	`
	_, err := p.db.Exec(query, id)

	return err
}

func (p *PostgresDB) GetUserRoles(id int64) ([]string, error) {
	query := `
		SELECT id, name, description
		FROM user_roles JOIN roles ON user_roles.role_id = roles.id
		WHERE user_roles.user_id = $1
	`

	var roles []string

	rows, err := p.db.Query(query, id)
	if err != nil {
		return nil, err
	}

	for rows.Next() {
		var r Role

		if err := rows.Scan(&r.ID, &r.Name, &r.Description); err != nil {
			return nil, err
		}
		roles = append(roles, r.Name)
	}

	if err := rows.Err(); err != nil {
		return nil, err
	}

	return roles, nil
}
