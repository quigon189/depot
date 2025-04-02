package repo

import (
	"database/sql"
	"log"

	_ "github.com/lib/pq"
	_ "github.com/mattn/go-sqlite3"
)

const (
	CreateUsersSQLite = `
	CREATE TABLE IF NOT EXISTS users (
		id            INTEGER PRIMARY KEY AUTOINCREMENT,
		name          TEXT UNIQUE,
		email         TEXT UNIQUE,
		password_hash TEXT
	);
	`
	CreateUsersPostgres = `
	CREATE TABLE IF NOT EXISTS users (
		id            SERIAL PRIMARY KEY,
		name          varchar(30) UNIQUE,
		email         varchar(50) UNIQUE,
		password_hash varchar(255)
	)
	`
	DropUsers        = `DROP TABLE IF EXISTS users`
	InsertUser       = `INSERT INTO users (name, email, password_hash) VALUES ($1, $2, $3) RETURNING id`
	SelectUsers      = `SELECT id, name, email FROM users`
	SelectUserByName = `SELECT id,name,email,password_hash FROM users WHERE name=$1`
)

type SqlRepo struct {
	db *sql.DB
}

func NewSqliteRepo(path string) Repo {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		log.Fatal("DB SQLite loaded")
	}
	log.Printf("DB %s connected", path)

	_, err = db.Exec(CreateUsersSQLite)
	if err != nil {
		log.Fatal("DDL error:", err)
	}

	return &SqlRepo{db: db}
}

func NewPostgreSQLRepo(connStr string) Repo {
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal("DB Postgres not loaded")
	}
	log.Print("PostgreSQL loaded")

	_, err = db.Exec(CreateUsersPostgres)
	if err != nil {
		log.Fatalf("Error create user table: %s", err.Error())
	}

	return &SqlRepo{db: db}
}

func (r *SqlRepo) Close(drop bool) {
	if drop {
		r.db.Exec(DropUsers)
	}
	r.db.Close()
}

func (r *SqlRepo) Add(u *User) (int, error) {
	var id int
	err := r.db.QueryRow(InsertUser, u.Name, u.Email, u.PasswordHash).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func (r *SqlRepo) GetByName(name string) (*User, error) {
	var u User
	err := r.db.QueryRow(SelectUserByName, name).Scan(&u.ID, &u.Name, &u.Email, &u.PasswordHash)
	if err != nil {
		return nil, err
	}

	return &u, nil
}
