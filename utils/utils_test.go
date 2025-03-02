package utils

import (
	"testing"
)

func TestSlugify(t *testing.T) {
	testCases := []struct {
		input    string
		expected string
	}{
		{"test", "test"},
		{"Test", "test"},
		{"Kanye West", "kanye-west"},
	}

	for _, tc := range testCases {
		t.Run(tc.input, func(t *testing.T) {
			actual := Slugify(tc.input)
			if actual != tc.expected {
				t.Errorf("Slugify(%s) is \"%s\", not \"%s\"", tc.input, actual, tc.expected)
			}
		})
	}
}
