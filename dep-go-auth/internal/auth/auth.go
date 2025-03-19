package auth

import (
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

const (
	TokenExpiration = time.Hour * 24 * 7
)

type Claims struct {
	UserID int `json:"user_id"`
	jwt.RegisteredClaims
}

type Auth struct {
	SecretKey []byte 
}

func (a *Auth) GenerateToken(userID int) (string, error) {
	claims := &Claims{
		UserID: userID,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(TokenExpiration)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "go-repo",
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	signedToken, err := token.SignedString(a.SecretKey)
	if err != nil {
		return "", errors.Join(errors.New("failed to generate token"), err)
	}

	return signedToken, nil
}
