package config

import (
	"flag"
	"fmt"
	"os"
	"log"

	"gopkg.in/yaml.v3"
)

type Config struct {
	Server struct {
		Host   string `yaml:"host"`
		Port   string `yaml:"port"`
		Secret string `yaml:"secret_key"`
	} `yaml:"server"`
}

func Fetch() *Config {
	path := fetchConfig()

	if err := validateConfig(path); err != nil {
		log.Fatalf("Validate error with config file: %s", err.Error())
	}

	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("Open error with config file: %s", err.Error())
	}
	defer file.Close()

	decoder := yaml.NewDecoder(file)

	var cfg Config
	if err = decoder.Decode(&cfg); err != nil {
		log.Fatalf("Decode error with config file: %s", err.Error())
	}

	return &cfg
}

func validateConfig(path string) error {
	stat, err := os.Stat(path)
	if err != nil {
		return err
	}

	if stat.IsDir() {
		return fmt.Errorf("%s is directory", path)
	}

	return nil
}

func fetchConfig() string {
	var path string

	flag.StringVar(&path, "config", "", "config yaml file for dep-go-auth service (default ./config.yml)")
	flag.Parse()

	if path == "" {
		path = os.Getenv("GO_AUTH_CONFIG")
	}

	if path == "" {
		path = "./config.yml"
	}

	return path
}
