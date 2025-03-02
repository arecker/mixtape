package download

import (
	"errors"
	"fmt"
	"os"
	"strings"

	"io"

	"github.com/kkdai/youtube/v2"
	"time"

	"github.com/arecker/mixtape/config"
	"github.com/arecker/mixtape/utils"
	"path/filepath"
)

func findVideoFormat(video *youtube.Video) (youtube.Format, error) {
	audioFormats := []youtube.Format{}
	for _, format := range video.Formats {
		if strings.HasPrefix(format.MimeType, "audio/") && format.AudioQuality != "" {
			audioFormats = append(audioFormats, format)
		}
	}

	if len(audioFormats) == 0 {
		return youtube.Format{}, fmt.Errorf("could not find an audio format for video")
	}

	return audioFormats[0], nil
}

func getVideoWithRetries(url string, maxTries int) (*youtube.Video, error) {
	currentTry := 0
	client := youtube.Client{}
	video := &youtube.Video{}

	for currentTry < maxTries {
		// delay
		time.Sleep(time.Duration(currentTry) * time.Second)

		video, err := client.GetVideo(url)
		if err != nil {

			// retry on 403
			if errors.Is(err, youtube.ErrUnexpectedStatusCode(403)) {
				currentTry += 1
				continue
			}

			// Retry on age restriction
			if errors.Is(err, youtube.ErrNotPlayableInEmbed) {
				currentTry += 1
				continue
			}

			// otherwise just return the error
			return video, fmt.Errorf("could not download video: %s", err)
		}

		return video, err
	}

	// tries expired
	return video, fmt.Errorf("exceeded %d max tries to download video", maxTries)
}

func getStreamWithRetries(video *youtube.Video, format youtube.Format, maxTries int) (io.ReadCloser, error) {
	currentTry := 0
	client := youtube.Client{}
	var stream io.ReadCloser

	for currentTry < maxTries {
		stream, _, err := client.GetStream(video, &format)
		if err != nil {
			// retry on 403
			if errors.Is(err, youtube.ErrUnexpectedStatusCode(403)) {
				fmt.Printf("got 403 from youtube (%d/%d tries)\n", currentTry+1, maxTries)
				currentTry += 1
				continue
			}

			// otherwise just return the error
			return stream, fmt.Errorf("could not download video stream: %s", err)
		}
		return stream, err
	}

	// tries expired
	return stream, fmt.Errorf("exceeded %d max tries to download video stream", maxTries)
}

func copyStreamWithRetries(file *os.File, stream io.ReadCloser, maxTries int) error {
	currentTry := 0

	for currentTry < maxTries {
		_, err := io.Copy(file, stream)
		if err != nil {
			// retry on 403
			if errors.Is(err, youtube.ErrUnexpectedStatusCode(403)) {
				fmt.Printf("got 403 from youtube (%d/%d tries)\n", currentTry+1, maxTries)
				time.Sleep(time.Duration(currentTry) * time.Second)
				currentTry += 1
				continue
			}

			// otherwise just return the error
			return fmt.Errorf("could not copy video stream: %s", err)
		}
		return nil
	}

	// tries expired
	return fmt.Errorf("exceeded %d max tries to download video stream", maxTries)
}

func DownloadTracks(tracks []config.Track) bool {
	if err := utils.EnsureDirectory("downloads"); err != nil {
		fmt.Printf("could not create downloads dir: %s\n", err)
		return false
	}

	// download each track
	success := true
	for _, track := range tracks {
		path := filepath.Join("downloads", track.Slug()+".m4a")
		if utils.FileExists(path) {
			continue
		}

		err := DownloadVideo(track.Youtube, path)
		if err != nil {
			success = false
			fmt.Printf("✗ [%s] %s\n", track.Name, err)
		} else {
			fmt.Printf("✓ [%s] downloaded (%s)\n", track.Name, path)
		}
	}

	return success
}

func DownloadVideo(url string, path string) error {
	// Download the video
	video, err := getVideoWithRetries(url, 5)
	if err != nil {
		return err
	}

	// Find the audio format
	format, err := findVideoFormat(video)
	if err != nil {
		return err
	}

	// get the stream from the video
	stream, err := getStreamWithRetries(video, format, 5)
	if err != nil {
		return fmt.Errorf("could not get stream from video: %s", err)
	}

	// create the file
	file, err := os.Create(path)
	if err != nil {
		return fmt.Errorf("could not create file: %s", err)
	}
	defer file.Sync()
	defer file.Close()

	// copy the stream to the file
	err = copyStreamWithRetries(file, stream, 5)
	if err != nil {
		return fmt.Errorf("could not write stream to file: %s", err)
	}

	return nil
}
