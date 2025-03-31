package auth

import (
	"db-go-auth/internal/repo"
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

const (
	TokenExpiration = time.Hour * 24 * 7
)

type Claims struct {
	UserID    int    `json:"user_id"`
	UserName  string `json:"user_name"`
	UserEmail string `json:"user_email"`
	jwt.RegisteredClaims
}

type Auth struct {
	SecretKey []byte
}

func (a *Auth) GenerateToken(user *repo.User) (string, error) {
	claims := &Claims{
		UserID:    user.ID,
		UserName:  user.Name,
		UserEmail: user.Email,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(TokenExpiration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "depot-user-repo",
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	signedToken, err := token.SignedString(a.SecretKey)
	if err != nil {
		return "", errors.Join(errors.New("failed to generate token"), err)
	}

	return signedToken, nil
}
