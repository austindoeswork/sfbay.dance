package app

import (
	"embed"
	"encoding/json"
	"io/ioutil"
	"log"
	"os"
)

//go:embed _ui/build
var UI embed.FS

// CONFIG

type Config struct {
	Env      string `json:"ENV"`
	Port     string `json:"PORT"`
	CertFile string `json:"CERTFILE"`
	KeyFile  string `json:"KEYFILE"`
}

func GetConfig() (*Config, error) {
	config_path := GetEnv("SFBAY_SERVER_CONFIG", "./server_config.json")
	log.Printf("loading config at:\n%s\n", config_path)

	file, err := ioutil.ReadFile(config_path)
	if err != nil {
		return nil, err
	}

	c := Config{}
	err = json.Unmarshal([]byte(file), &c)
	if err != nil {
		return nil, err
	}

	log.Printf("config loaded:\n%+v\n", c)

	return &c, nil
}

// MISC.

func GetEnv(key, fallback string) string {
	value := os.Getenv(key)
	if len(value) == 0 {
		return fallback
	}
	return value
}
