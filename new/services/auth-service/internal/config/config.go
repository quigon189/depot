package config

import (
	"os"
	"time"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Server   ServerConfig  `yaml:"server"`
	Logging  LoggingConfig `yaml:"logging"`
	Database DBConfig      `yaml:"database"`
	JWT      JWTConfig     `yaml:"jwt"`
}

type JWTConfig struct {
	Secret             string        `yaml:"secret"`
	AccessTokenExpiry  time.Duration `yaml:"access_token_expiry"`
	RefreshTokenExpiry time.Duration `yaml:"refresh_token_expiry"`
}

type ServerConfig struct {
	Address  string `yaml:"address"`
	GRPCPort string `yaml:"grpc_port"`
	HTTPPort string `yaml:"http_port"`
}

type DBConfig struct {
	Host           string `yaml:"host"`
	Port           int    `yaml:"port"`
	User           string `yaml:"user"`
	Password       string `yaml:"password"`
	Name           string `yaml:"name"`
	MigrationsPath string `yaml:"migrations_path"`
}

type LoggingConfig struct {
	Level  string `yaml:"level"`
	Format string `yaml:"format"`
}

func GetConfig(path string) (*Config, error) {
	data, err := os.ReadFile(path)

	if err != nil {
		return nil, err
	}

	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		return nil, err
	}

	return &cfg, nil
}
