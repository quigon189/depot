package service

import (
	"auth-service/internal/database"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
)

type UserClaims struct {
	UserID    int64    `json:"id"`
	UserEmail string   `json:"email"`
	UserRoles []string `json:"roles"`
	jwt.RegisteredClaims
}

func (s *AuthService) generateAccessToken(user *database.User, roles []string) (string, error) {
	claims := UserClaims{
		UserID:    user.ID,
		UserEmail: user.Email,
		UserRoles: roles,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(time.Now().Add(s.accessTokenExpiry)),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Issuer:    "depot-auth-service",
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)

	signedToken, err := token.SignedString(s.jwtSecret)
	if err != nil {
		return "", errors.New("failed to generate token: " + err.Error())
	}

	return signedToken, nil
}

func (s *AuthService) generateRefreshToken(user *database.User) (string, error) {
	expiresAt := time.Now().Add(s.refreshTokenExpiry)

	tokenBytes := make([]byte, 32)
	if _, err := rand.Read(tokenBytes); err != nil {
		return "", err
	}

	token := base64.RawURLEncoding.EncodeToString(tokenBytes)

	refreshToken := &database.RefreshToken{
		Token:     token,
		UserID:    user.ID,
		ExpiresAt: expiresAt,
		CreatedAt: time.Now(),
	}

	if err := s.db.SaveRefreshToken(refreshToken); err != nil {
		return "", errors.New("failed to generate refresh token: " + err.Error())
	}

	return token, nil
}

func (s *AuthService) validateJWT(tokenString string) (*UserClaims, error) {
	token, err := jwt.Parse(
		tokenString,
		func(token *jwt.Token) (interface{}, error) {
			if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
				return nil, errors.New("uncorect signing method")
			}

			return []byte(s.jwtSecret), nil
		},
	)

	if err != nil {
		return nil, errors.New("failed to parse token")
	}

	if claims, ok := token.Claims.(*UserClaims); ok && token.Valid {
		if !claims.VerifieSx
	}
}
