package main

import (
	"fmt"
	"os"

	"github.com/arecker/mixtape/config"
	"github.com/arecker/mixtape/convert"
	"github.com/arecker/mixtape/download"
	"time"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Printf("Usage: mixtape <path/to/album.yml>\n")
		os.Exit(1)
	}

	c, err := config.NewConfig(os.Args[1])
	if err != nil {
		fmt.Printf("could not load config: %s\n", err)
		os.Exit(1)
	}

	for true {
		if download.DownloadTracks(c.Tracks) {
			break
		}
		fmt.Printf("download failed, retrying...\n")
		time.Sleep(10 * time.Second)
	}

	if !convert.ConvertTracks(c.Tracks) {
		os.Exit(1)
	}
}
