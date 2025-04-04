package config

import (
	"flag"
	"log"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
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

func (cfg *Config) Fetch() {
	path := configPath()

	cfgBytes, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Error reading config file path=%s: %s", path, err.Error())
	}

	cfgLines := strings.Split(string(cfgBytes), "\n")
	for n, line := range cfgLines {
		envIdx := strings.Index(line, "$")
		if envIdx > 0 {
			env := strings.Split(line[envIdx+1:], " ")[0]
			cfgLines[n] = line[:envIdx] + os.Getenv(env) 
			log.Printf("%v: %s\t%s", n, line, env)
		}
	}

	log.Println(cfgLines)

	if err = yaml.Unmarshal([]byte(strings.Join(cfgLines, "\n")), cfg); err != nil {
		log.Fatalf("Error unmarshal %s file: %s", path, err.Error())
	}

}

func configPath() string {
	var path string

	flag.StringVar(&path, "config", "", "path to config.yaml file (default ./config.yml)")
	flag.Parse()

	if path == "" {
		var ok bool
		path, ok = os.LookupEnv("CATALOG_CONFIG")
		if !ok {
			path = "./config.yml"
		}
	}

	stat, err := os.Stat(path)
	if err != nil {
		log.Fatalf("Error get stat path=%s: %s", path, err.Error())
	}

	if stat.IsDir() {
		log.Fatalf("Error path=%s is directory", path)
	}

	return path
}
