package utils

import (
	"os"
	"path/filepath"
	"strings"
)

// Return a slug version of a string
func Slugify(word string) string {
	// make lowercase
	word = strings.ToLower(word)

	// Replace spaces with dashes
	word = strings.Replace(word, " ", "-", -1)

	return word
}

func EnsureDirectory(name string) error {
	dirpath := filepath.Join(".", name)
	err := os.MkdirAll(dirpath, os.ModePerm)
	if err != nil {
		return err
	}
	return nil
}

func ClearDirectory(target string, glob string) error {
	matches, err := filepath.Glob(filepath.Join(target, glob))
	if err != nil {
		return err
	}
	for _, m := range matches {
		if err := os.Remove(m); err != nil {
			return err
		}
	}
	return nil
}

func FileExists(path string) bool {
	_, err := os.Stat(path)
	return err == nil
}
