package service

import (
	"auth-service/internal/database"
	"auth-service/internal/grpc/auth_grpc"
	"context"
	"errors"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type AuthService struct {
	db *database.PostgresDB
	jwtSecret string
	tokenExpiry time.Duration
}

func NewAuthService(db *database.PostgresDB, jwt string, tokenExpiry time.Duration) *AuthService {
	return &AuthService{
		db: db,
		jwtSecret: jwt,
		tokenExpiry: tokenExpiry,
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

	accessToken, err := s.generateAccessToken(user)
	if err != nil {
		return nil, errors.New("failed to generate token")
	}

	refreshToken, err := s.generateRefreshToken(user, req.UserAgent)
	if err != nil {
		return nil, errors.New("failed to generate token")
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		return nil, errors.New("failed to get user roles")
	}

	return &auth_grpc.LoginResponse{
		Token: accessToken,
		RefreshToken: refreshToken,
		ExpiresAt: int64(s.tokenExpiry),
		User: &auth_grpc.User{
			Id: user.ID,
			Username: user.Username,
			Email: user.Email,
			Roles: roles,
		},
	}, nil
}
