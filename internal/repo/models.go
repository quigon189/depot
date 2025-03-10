package repo

import (
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID           int    `json:"id"`
	Name         string `json:"name"`
	Email        string `json:"email"`
	PasswordHash string `json:"-"`
}

func NewUser(name, email, passord string) (*User, error) {
	u := User{}

	u.Name = name
	err := u.SetPassword(passord)
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
