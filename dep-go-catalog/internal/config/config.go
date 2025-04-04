package config

import (
	"bufio"
	"bytes"
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


func Fetch() *Config {
	path := configPath()

	file, err := os.Open(path)
	if err != nil {
		log.Fatalf("Error open config file, path=%s: %s", path, err.Error())
	}
	defer file.Close()

	wr := bytes.Buffer{}
	sc := bufio.NewScanner(file)
	for sc.Scan() {
		wr.WriteString(sc.Text())
	}

	//decoder := yaml.NewDecoder(file)

	cfgStr := wr.String()

	cfgLines := strings.Split(cfgStr, "\n")
	fmt.Println(cfgLines)

	var cfg Config
	yaml.Unmarshal([]byte(cfgStr), &cfg)
	// if err = decoder.Decode(&cfg); err != nil {
	// 	log.Fatalf("Error decode %s file: %s", path, err.Error())
	// }

	return &cfg
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
	if err!=nil {
		log.Fatalf("Error get stat path=%s: %s",path,err.Error())
	}

	if stat.IsDir() {
		log.Fatalf("Error path=%s is directory", path)
	}

	return path
}
