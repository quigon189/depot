//Пакет для полученя конфигурации из yaml файла с подстановкой переменных окружения
package ymlconfig

import (
	"flag"
	"fmt"
	"log"
	"os"
	"strings"

	"gopkg.in/yaml.v3"
)
//Базовая структура, содержащая источники получения пути к файлу конфигурации
type YMLCfg struct {
	//Флаг командной строки, если пустое значение, то подставляется "config"
	Flag string
	//Переменная окружения, если пустое значение, то подставляется "CONFIG_PATH"
	Env  string
	//Значение по умолчанию, если не будут указаны флаг и переменная окружения
	//Если пустое значение, то подставится "./config.yml"
	Def  string
}

func New(flag, env, def string) *YMLCfg {
	var cfg YMLCfg

	cfg.Flag = flag
	cfg.Env = env
	cfg.Def = def

	return &cfg
}

//Получить конфигурацию из источников указаных в структуре YMLCfg
//Так же, перед размаршаливанием, происходит подмена переменных окружения
//Порядок перебора источников (значение по умолчанию):
//    1. Флаг командной строки YMLCfg.Flag (config)
//    2. Переменная окружения YMLCfg.Env (CONFIG_PATH)
//    3. Путь по умолчанию YMLCfg.Def (./config.yml)
func (c *YMLCfg) Fetch(cfg any) {
	path := c.configPath()

	cfgBytes, err := os.ReadFile(path)
	if err != nil {
		log.Fatalf("Error reading config file path=%s: %s", path, err.Error())
	}

	cfgLines := strings.Split(string(cfgBytes), "\n")
	for n, line := range cfgLines {
		envIdx := strings.Index(line, "${")
		if envIdx > 0 {
			env := strings.Split(line[envIdx+2:], "}")[0]
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
