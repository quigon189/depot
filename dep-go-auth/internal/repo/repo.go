package repo

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/mattn/go-sqlite3"
)

const (
	DropUsers   = `DROP TABLE IF EXISTS users`
	CreateUsers = `
	CREATE TABLE IF NOT EXISTS users (
		id            INTEGER PRIMARY KEY AUTOINCREMENT,
		name          TEXT UNIQUE,
		email         TEXT UNIQUE,
		password_hash TEXT UNIQUE
	);
	`
	InsertUser       = `INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?) RETURNING id;`
	SelectUsers      = `SELECT id, name, email FROM users`
	SelectUserByName = `SELECT id,name,email,password_hash FROM users WHERE name=?`
)

type Repo interface {
	Close(drop bool)
	Add(u *User) (int, error)
	GetAll() ([]User, error)
	GetByName(name string) (*User, error)
}

type UserRepo struct {
	db *sql.DB
}

func NewUserRepo(path string) Repo {
	db, err := sql.Open("sqlite3", path)
	if err != nil {
		panic("DB not loaded")
	}
	fmt.Println("DB connected")

	_, err = db.Exec(CreateUsers)
	if err != nil {
		log.Fatal("DDL error:", err)
	}

	return &UserRepo{db: db}
}

func (r *UserRepo) Close(drop bool) {
	if drop {
		r.db.Exec(DropUsers)
	}
	r.db.Close()
}

func (r *UserRepo) Add(u *User) (int, error) {
	var id int
	err := r.db.QueryRow(InsertUser, u.Name, u.Email, u.PasswordHash).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func (r *UserRepo) GetAll() ([]User, error) {
	result := make([]User, 0)

	rows, err := r.db.Query(SelectUsers)
	if err != nil {
		return nil, err
	}

	for rows.Next() {
		var u User

		err = rows.Scan(&u.ID, &u.Name, &u.Email)
		if err != nil {
			return nil, err
		}

		result = append(result, u)
	}

	return result, nil
}

func (r *UserRepo) GetByName(name string) (*User, error) {
	var u User
	err := r.db.QueryRow(SelectUserByName, name).Scan(&u.ID, &u.Name, &u.Email, &u.PasswordHash)
	if err != nil {
		return nil, err
	}

	return &u, nil

}
