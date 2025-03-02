package convert

import (
	"fmt"
	"os/exec"

	"path/filepath"

	"github.com/arecker/mixtape/config"
	"github.com/arecker/mixtape/utils"
)

func ConvertTracks(tracks []config.Track) bool {
	// create directory
	if err := utils.EnsureDirectory("export"); err != nil {
		fmt.Printf("could not create export dir: %s\n", err)
		return false
	}

	// clear out directory
	if err := utils.ClearDirectory("./export", "*.ogg"); err != nil {
		fmt.Printf("could not clear export dir: %s\n", err)
		return false
	}

	// convert each track
	success := true
	for i, track := range tracks {
		src := filepath.Join("downloads", track.Slug()+".m4a")
		if !utils.FileExists(src) {
			fmt.Printf("✗ [%s] could not convert, download does not exist\n", track.Name)
			success = false
			continue
		}
		dst := filepath.Join("export", track.ExportFileName(i+1))
		err := ConvertToOgg(src, dst)
		if err != nil {
			success = false
			fmt.Printf("✗ [%s] could not convert: %s\n", track.Name, err)
		} else {
			fmt.Printf("✓ [%s] converted (%s)\n", track.Name, dst)
		}
	}
	return success
}

func ConvertToOgg(src string, dst string) error {
	cmd := exec.Command("ffmpeg", "-i", src, dst)
	err := cmd.Run()
	if err != nil {
		return fmt.Errorf("failed to convert %s to %s: %s", src, dst, err)
	}
	return nil
}
