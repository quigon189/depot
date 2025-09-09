package service

import (
	"auth-service/internal/database"
	"auth-service/internal/grpc/auth_grpc"
	"context"
	"crypto/rand"
	"encoding/base64"
	"errors"
	"time"

	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"
)

type AuthService struct {
	db                 *database.PostgresDB
	jwtSecret          string
	accessTokenExpiry  time.Duration
	refreshTokenExpiry time.Duration
}

func NewAuthService(db *database.PostgresDB, jwtSecret string, atokenExpiry time.Duration, rtokenExpiry time.Duration) *AuthService {
	return &AuthService{
		db:                 db,
		jwtSecret:          jwtSecret,
		accessTokenExpiry:  atokenExpiry,
		refreshTokenExpiry: rtokenExpiry,
	}
}

func (s *AuthService) Login(ctx context.Context, req auth_grpc.LoginRequest) (*auth_grpc.LoginResponse, error) {
	user, err := s.db.GetUserByLogin(req.Login)
	if err != nil {
		return nil, errors.New("invalid credentials")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password)); err != nil {
		return nil, errors.New("invalid credentials")
	}

	if !user.IsActive {
		return nil, errors.New("account is deavtivated")
	}

	if err := s.db.UpdateLastLogin(user.ID); err != nil {
		return nil, errors.New("failed to update login time")
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		return nil, errors.New("failed to get user roles")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		return nil, errors.New("failed to generate token")
	}

	refreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		return nil, errors.New("failed to generate token")
	}

	return &auth_grpc.LoginResponse{
		Token:        accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    int64(s.accessTokenExpiry),
		User: &auth_grpc.User{
			Id:    user.ID,
			Email: user.Email,
			Roles: roles,
		},
	}, nil
}

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

	refreshToken := database.RefreshToken{
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
