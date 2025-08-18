package confihjhj

import (
	"os"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Server struct {
		Address string `yaml:"address"`
		Port    string `yaml:"port"`
	} `yaml:"server"`
}

func GetConfig(path string) *Config {
	data, _ := os.ReadFile(path)
	var cfg Config
	yaml.Unmarshal(data, &cfg)
	return &cfg
}
