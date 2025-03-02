package config

import (
	"fmt"
	"os"

	"gopkg.in/yaml.v2"

	"github.com/arecker/mixtape/utils"
	"strings"
)

type Track struct {
	Name    string
	Artist  string
	Youtube string
}

func (t *Track) Slug() string {
	return fmt.Sprintf("%s-%s", utils.Slugify(t.Artist), utils.Slugify(t.Name))
}

func (t *Track) ExportFileName(trackno int) string {
	// title in all caps
	title := strings.ToUpper(t.Name)
	return fmt.Sprintf("%02d - %s.ogg", trackno, title)
}

type Config struct {
	Name   string
	Tracks []Track
}

func NewConfig(path string) (*Config, error) {
	var config Config
	file, err := os.ReadFile(path)
	if err != nil {
		return &config, fmt.Errorf("could not read config from %s: %s", path, err)
	}
	err = yaml.Unmarshal(file, &config)
	if err != nil {
		return &config, fmt.Errorf("could not read unmashal config: %s", err)
	}

	return &config, nil
}
