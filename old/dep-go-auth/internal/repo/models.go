package repo

import (
	"errors"
	"net/mail"
	"slices"

	"golang.org/x/crypto/bcrypt"
)

var roles = []string{"admin", "student", "teacher", "manager"}

type User struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	Email        string `json:"email"`
	Role         string `json:"role"`
	PasswordHash string `json:"-"`
}

func NewUser(name, email, password, role string) (*User, error) {
	u := User{}

	if len([]rune(name)) < 3 {
		return nil, errors.New("name must be at least 3 charecters long")
	}

	if len([]rune(password)) < 8 {
		return nil, errors.New("password must be at least 8 characters long")
	}

	_, err := mail.ParseAddress(email)
	if err != nil {
		return nil, errors.New("bad email")
	}

	if !slices.Contains(roles, role) {
		return nil, errors.New("bad role")
	}

	u.Name = name
	u.Email = email
	u.Role = role
	err = u.SetPassword(password)
	if err != nil {
		return nil, err
	}

	return &u, nil
}

func (u *User) SetPassword(password string) error {
	hash, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	if err != nil {
		return err
	}
	u.PasswordHash = string(hash)
	return nil
}

func (u *User) CheckPassword(password string) bool {
	err := bcrypt.CompareHashAndPassword([]byte(u.PasswordHash), []byte(password))
	return err == nil
}
