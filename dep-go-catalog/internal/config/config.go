package config

import (
	"dep-go-catalog/pkg/ymlconfig"
)

type Config struct {
	Server struct {
		Host string `yaml:"host"`
		Port string `yaml:"port"`
	} `yaml:"server"`

	Secret string `yaml:"secret_key"`

	DB struct {
		Name string `yaml:"name"`
		Host string `yaml:"host"`
		Port string `yaml:"port"`
		User string `yaml:"user"`
		Pass string `yaml:"password"`
	} `yaml:"database"`
}

func FetchConfig() *Config {
	var cfg Config
	var c ymlconfig.YMLCfg

	c.Fetch(&cfg)

	return &cfg
}
