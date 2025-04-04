package main

import (
	"dep-go-catalog/internal/config"
	"log"
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

func main() {

	var cfg Config
	var c config.YMLCfg
	c.Fetch(&cfg)

	log.Printf("%+v", cfg)
	log.Fatalf("server %s:%s stoped", cfg.Server.Host, cfg.Server.Port)
}
