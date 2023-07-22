package app

import (
	"embed"
	"encoding/json"
	"io/ioutil"
)

//go:embed _ui/build
var UI embed.FS

// CONFIG

type Config struct {
	Env  string `json:"ENV"`
	Port string `json:"PORT"`
}

func GetConfig() (*Config, error) {
	file, err := ioutil.ReadFile("./server_config.json")
	if err != nil {
		return nil, err
	}

	c := Config{}
	err = json.Unmarshal([]byte(file), &c)
	if err != nil {
		return nil, err
	}

	return &c, nil
}
