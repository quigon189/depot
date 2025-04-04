package config

import (
	"flag"
	"fmt"
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

type YMLCfg struct {
	Flag string
	Env  string
	Def  string
}

func New(flag, env, def string) *YMLCfg {
	var cfg YMLCfg
	if flag == "" {
		flag = "config"
	}

	if env == "" {
		env = "CONFIG_PATH"
	}

	if def == "" {
		def = "./config.yml"
	}
	cfg.Flag = flag
	cfg.Env = env
	cfg.Def = def

	return &cfg
}

func (c *YMLCfg) Fetch(cfg any) {
	path := c.configPath()

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
		}
	}

	if err = yaml.Unmarshal([]byte(strings.Join(cfgLines, "\n")), cfg); err != nil {
		log.Fatalf("Error unmarshal %s file: %s", path, err.Error())
	}

}

func (cfg *YMLCfg) configPath() string {
	if cfg.Flag == "" {
		cfg.Flag = "config"
	}

	if cfg.Env == "" {
		cfg.Env = "CONFIG_PATH"
	}

	if cfg.Def == "" {
		cfg.Def = "./config.yml"
	}
	var path string

	flag.StringVar(&path, cfg.Flag, "", fmt.Sprintf("path to config.yaml file (default %s)", cfg.Def))
	flag.Parse()

	if path == "" {
		var ok bool
		path, ok = os.LookupEnv(cfg.Env)
		if !ok {
			path = cfg.Def 
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
