package auth

import (
	"api-gateway-service/internal/config"
	"api-gateway-service/internal/grpc/auth_grpc"
	"context"
	"log"
	"time"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

type GRPCClient struct {
	client auth_grpc.AuthServiceClient
	conn   *grpc.ClientConn
	config config.GRPCServiceConfig
}

func NewGRPCClient(cfg config.GRPCServiceConfig) (*GRPCClient, error) {
	var opts []grpc.DialOption

	opts = append(opts, grpc.WithTransportCredentials(insecure.NewCredentials()))
	opts = append(opts, grpc.WithUnaryInterceptor(grpcUnaryInterceptor))
	opts = append(opts, grpc.WithStreamInterceptor(grpcStreamInterceptor))

	conn, err := grpc.NewClient(cfg.Address, opts...)
	if err != nil {
		return nil, err
	}

	// ctx, cancel := context.WithTimeout(context.Background(), cfg.Timeout)
	// defer cancel()
	//
	// if !conn.WaitForStateChange(ctx, conn.GetState()) {
	// 	return nil, errors.New("failed to connect to " + cfg.Address)
	// }
	//
	client := auth_grpc.NewAuthServiceClient(conn)

	return &GRPCClient{
		client: client,
		conn:   conn,
		config: cfg,
	}, err
}

func (c *GRPCClient) Close() error {
	return c.conn.Close()
}

func (c *GRPCClient) Login(ctx context.Context, req *auth_grpc.LoginRequest) (*auth_grpc.LoginResponse, error) {
	ctx, cancel := context.WithTimeout(ctx, c.config.Timeout)
	defer cancel()

	return c.client.Login(ctx, req)
}

func (c *GRPCClient) Register(ctx context.Context, req *auth_grpc.RegisterRequest) (*auth_grpc.RegisterResponse, error) {
	ctx, cancel := context.WithTimeout(ctx, c.config.Timeout)
	defer cancel()

	return c.client.Register(ctx, req)
}

func (c *GRPCClient) ValidateToken(ctx context.Context, req *auth_grpc.ValidateTokenRequest) (*auth_grpc.ValidateTokenResponse, error) {
	ctx, cancel := context.WithTimeout(ctx, c.config.Timeout)
	defer cancel()

	return c.client.ValidateToken(ctx, req)
}

func (c *GRPCClient) RefreshToken(ctx context.Context, req *auth_grpc.RefreshTokenRequest) (*auth_grpc.RefreshTokenResponse, error) {
	ctx, cancel := context.WithTimeout(ctx, c.config.Timeout)
	defer cancel()

	return c.client.RefreshToken(ctx, req)
}

func grpcUnaryInterceptor(ctx context.Context, method string, req, reply interface{}, cc *grpc.ClientConn, invoker grpc.UnaryInvoker, opts ...grpc.CallOption) error {
	start := time.Now()
	err := invoker(ctx, method, req, reply, cc, opts...)
	duration := time.Since(start)

	if err != nil {
		log.Printf("gRPC call failed: %s, duration: %v, error: %v", method, duration, err)
	} else {
		log.Printf("gRPC call successed: %s, duration %v", method, duration)
	}

	return err
}

func grpcStreamInterceptor(ctx context.Context, desc *grpc.StreamDesc, cc *grpc.ClientConn, method string, streamer grpc.Streamer, opts ...grpc.CallOption) (grpc.ClientStream, error) {
	start := time.Now()
	clientStream, err := streamer(ctx, desc, cc, method, opts...)
	duration := time.Since(start)

	if err != nil {
		log.Printf("gRPC stream failed: %s, duration %v, error: %v", method, duration, err)
	} else {
		log.Printf("gRPC stream successed: %s, duration %v", method, duration)
	}

	return clientStream, err
}
