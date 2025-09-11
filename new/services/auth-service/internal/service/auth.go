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

func (s *AuthService) Login(ctx context.Context, req *auth_grpc.LoginRequest) (*auth_grpc.LoginResponse, error) {
	user, err := s.db.GetUserByLogin(req.Login)
	if err != nil {
		return nil, errors.New("invalid credentials")
	}

	if !user.IsVerified {
		return nil, errors.New("account is not verified")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password)); err != nil {
		return nil, errors.New("invalid credentials")
	}

	if !user.IsActive {
		return nil, errors.New("account is deavtivated")
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

	if err := s.db.UpdateLastLogin(user.ID); err != nil {
		return nil, errors.New("failed to update login time")
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

func (s *AuthService) Register(ctx context.Context, req *auth_grpc.RegisterRequest) (*auth_grpc.RegisterResponse, error) {
	if exists := s.db.UserExists(req.Email); exists {
		return nil, errors.New("user alredy exists")
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		return nil, errors.New("failed to hash password")
	}

	user := &database.User{
		Email:        req.Email,
		PasswordHash: string(passwordHash),
		IsActive:     true,
		IsVerified:   false,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}

	user, err = s.db.CreateUser(user)
	if err != nil {
		return nil, errors.New("failed to create user")
	}

	role := "user"

	roles, err := s.db.AssignRoleToUser(user.ID, role)
	if err != nil {
		return nil, errors.New("failed to assign role")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		return nil, errors.New("failed to generate token")
	}

	refreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		return nil, errors.New("failed to generate refresh token")
	}

	return &auth_grpc.RegisterResponse{
		Token:        accessToken,
		RefreshToken: refreshToken,
		ExpiresAt:    time.Now().Add(s.refreshTokenExpiry).Unix(),
		User: &auth_grpc.User{
			Id:    user.ID,
			Email: user.Email,
			Roles: roles,
		},
	}, nil
}

func (s *AuthService) ValidateToken(ctx context.Context, req *auth_grpc.ValidateTokenRequest) (*auth_grpc.ValidateTokenResponse, error) {
	claims, err := s.validateJWT(req.Token)
	if err != nil {
		return &auth_grpc.ValidateTokenResponse{Valid: false}, err
	}

	user, err := s.db.GetUserByLogin(claims.UserEmail)
	if err != nil {
		return &auth_grpc.ValidateTokenResponse{Valid: false}, err
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		return &auth_grpc.ValidateTokenResponse{Valid: false}, err
	}

	return &auth_grpc.ValidateTokenResponse{
		Valid: true,
		User: &auth_grpc.User{
			Id:    user.ID,
			Email: user.Email,
			Roles: roles,
		},
	}, nil
}

func (s *AuthService) RefreshToken(ctx context.Context, req *auth_grpc.RefreshTokenRequest) (*auth_grpc.RefreshTokenResponse, error) {
	refreshToken, err := s.db.GetRefreshToken(req.RefreshToken)
	if err != nil {
		return nil, errors.New("invalid refresh token")
	}

	if !refreshToken.RevokedAt.IsZero() {
		return nil, errors.New("refresh token revoked")
	}

	if time.Now().After(refreshToken.ExpiresAt) {
		return nil, errors.New("refresh token expired")
	}

	user, err := s.db.GetUserByID(refreshToken.UserID)
	if err != nil || !user.IsActive {
		return nil, errors.New("user not found or inactive")
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		return nil, errors.New("failed to get user roles")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		return nil, errors.New("failed to generate access token")
	}

	newRefreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		return nil, errors.New("failed to generate refresh token")
	}

	if err := s.db.RevokeRefreshToken(req.RefreshToken); err != nil {
		return nil, errors.New("failed to revoke refresh token")
	}

	return &auth_grpc.RefreshTokenResponse{
		Token: accessToken,
		RefreshToken: newRefreshToken,
		ExpiresAt: time.Now().Add(s.refreshTokenExpiry).Unix(),
	}, nil
}
