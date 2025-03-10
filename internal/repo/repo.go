package repo

import (
	"database/sql"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
)

const (
	DropUsers = `DROP TABLE IF EXISTS users`
	CreateUsers = `
	CREATE TABLE IF NOT EXISTS users (
		id            INTEGER PRIMARY KEY AUTOINCREMENT,
		name          TEXT,
		password_hash TEXT
	);
	`
	InsertUser  = `INSERT INTO users (name, password_hash) VALUES (?, ?) RETURNING id;`
	SelectUsers = `SELECT id, name FROM users`
	SelectUserByName = `SELECT id,name,password_hash FROM users WHERE name=?`
)

type Repo struct {
	db *sql.DB
}

func NewRepo(path string) *Repo {
	r := Repo{}

	db, err := sql.Open("sqlite3", path)
	if err != nil {
		panic("DB not loaded")
	}
	fmt.Println("DB connected")

	_, err = db.Exec(CreateUsers)
	if err != nil {
		panic("DDL error")
	}

	r.db = db

	return &r
}

func (r *Repo) Close() {
	r.db.Close()
}

func (r *Repo) UserAdd(u *User) (int, error) {
	var id int
	err := r.db.QueryRow(InsertUser, u.Name, u.PasswordHash).Scan(&id)
	if err != nil {
		return -1, err
	}
	return id, nil
}

func (r *Repo) UserGetAll() ([]User, error) {
	result := make([]User, 0)

	rows, err := r.db.Query(SelectUsers)
	if err != nil {
		return nil, err
	}

	for rows.Next() {
		var u User
		
		err = rows.Scan(&u.ID, &u.Name)
		if err != nil {
			return nil, err
		}

		result = append(result, u)	
	}

	return result, nil
}

func (r *Repo) UserGetByName(name string) (*User, error) {
	var u User
	err := r.db.QueryRow(SelectUserByName, name).Scan(&u.ID, &u.Name, &u.PasswordHash)
	if err != nil {
		return nil, err
	}

	return &u, nil
	
}
