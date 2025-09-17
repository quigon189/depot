package service

import (
	"auth-service/internal/database"
	"auth-service/internal/grpc/auth_grpc"
	"context"
	"log"
	"time"

	"golang.org/x/crypto/bcrypt"
	"google.golang.org/grpc/codes"
	"google.golang.org/grpc/status"
)

type AuthService struct {
	auth_grpc.UnimplementedAuthServiceServer
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
		log.Printf("Failed to get user: %v error: invalid email", req.Login)
		return nil, status.Errorf(codes.Unauthenticated, "invalid credentials")
	}

	if !user.IsVerified {
		log.Printf("User not verified: %v", req.Login)
		return nil, status.Errorf(codes.Unauthenticated, "account is not verified")
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.PasswordHash), []byte(req.Password)); err != nil {
		log.Printf("Failed to get user: %v error: invalid password", req.Login)
		return nil, status.Errorf(codes.Unauthenticated, "invalid credentials")
	}

	if !user.IsActive {
		log.Printf("User not active: %v", req.Login)
		return nil, status.Errorf(codes.Unauthenticated, "account is deavtivated")
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		log.Printf("Failed to get user roles: %v error: %v", req.Login, err)
		return nil, status.Errorf(codes.Internal, "failed to get user roles")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		log.Printf("Failed to generate access token: %v error: %v", req.Login, err)
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	refreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		log.Printf("Failed to generate refresh token: %v error: %v", req.Login, err)
		return nil, status.Errorf(codes.Internal, err.Error())
	}

	if err := s.db.UpdateLastLogin(user.ID); err != nil {
		log.Printf("Failed to update login time: %v error: %v", req.Login, err)
		return nil, status.Errorf(codes.Internal, "failed to update login time")
	}

	log.Printf("User logined: %v", user.Email)

	return &auth_grpc.LoginResponse{
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

func (s *AuthService) Register(ctx context.Context, req *auth_grpc.RegisterRequest) (*auth_grpc.RegisterResponse, error) {
	if exists := s.db.UserExists(req.Email); exists {
		log.Printf("filed to register user: user already exists: %v", req.Email)
		return nil, status.Errorf(codes.AlreadyExists, "user alredy exists")
	}

	passwordHash, err := bcrypt.GenerateFromPassword([]byte(req.Password), bcrypt.DefaultCost)
	if err != nil {
		log.Printf("failed to hash password with user: %v error: %v", req.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to hash password")
	}

	user := &database.User{
		Email:        req.Email,
		PasswordHash: string(passwordHash),
		IsActive:     true,
		IsVerified:   true,
		CreatedAt:    time.Now(),
		UpdatedAt:    time.Now(),
	}

	user, err = s.db.CreateUser(user)
	if err != nil {
		log.Printf("failed to create user: %v error: %v", req.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to create user")
	}

	role := "user"

	roles, err := s.db.AssignRoleToUser(user.ID, role)
	if err != nil {
		log.Printf("failed to assign role with user: %v, %v error: %v", req.Email, role, err)
		return nil, status.Errorf(codes.Internal, "failed to assign role")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		log.Printf("failed to generate access token with user: %v error: %v", req.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to generate access token")
	}

	refreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		log.Printf("failed to generate refresh token with user: %v error: %v", req.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to generate refresh token")
	}

	log.Printf("registred user email: %s with roles %v:", user.Email, roles)

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
		log.Printf("Failed to validate jwt: %v error: %v", req.Token, err)
		return &auth_grpc.ValidateTokenResponse{
			Valid: false,
			User: &auth_grpc.User{},
		}, nil
	}

	user, err := s.db.GetUserByLogin(claims.UserEmail)
	if err != nil {
		log.Printf("Failed to get user on validation: %v error: %v", claims.UserEmail, err)
		return &auth_grpc.ValidateTokenResponse{Valid: false}, status.Errorf(codes.InvalidArgument, err.Error())
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		log.Printf("Failed to get user roles on validation: %v error: %v", claims.UserEmail, err)
		return &auth_grpc.ValidateTokenResponse{Valid: false}, status.Errorf(codes.InvalidArgument, err.Error())
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
		log.Printf("Failed validate refresh token: %v error: %v", req.RefreshToken, err)
		return nil, status.Errorf(codes.Unauthenticated, "failed to validate refresh token")
	}

	if time.Now().After(refreshToken.ExpiresAt) {
		log.Printf("Refresh token expired: %v", req.RefreshToken)
		return nil, status.Errorf(codes.Unauthenticated, "refresh token expired")
	}

	user, err := s.db.GetUserByID(refreshToken.UserID)
	if err != nil || !user.IsActive {
		log.Printf("Failed to get user on refresh token: %v error: %v", req.RefreshToken, err)
		return nil, status.Errorf(codes.Unauthenticated, "user not found or inactive")
	}

	roles, err := s.db.GetUserRoles(user.ID)
	if err != nil {
		log.Printf("Failed to get user roles on refresh token: %v error: %v", user.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to get user roles")
	}

	accessToken, err := s.generateAccessToken(user, roles)
	if err != nil {
		log.Printf("Failed to generate access token: %v error: %v", user.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to generate access token")
	}

	newRefreshToken, err := s.generateRefreshToken(user)
	if err != nil {
		log.Printf("Failed to generate refresh token: %v error: %v", user.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to generate refresh token")
	}

	if err := s.db.RevokeRefreshToken(req.RefreshToken); err != nil {
		log.Printf("Failed to revoke refresh token: %v error: %v", user.Email, err)
		return nil, status.Errorf(codes.Internal, "failed to revoke refresh token")
	}

	return &auth_grpc.RefreshTokenResponse{
		Token:        accessToken,
		RefreshToken: newRefreshToken,
		ExpiresAt:    time.Now().Add(s.refreshTokenExpiry).Unix(),
	}, nil
}
