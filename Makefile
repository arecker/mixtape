.PHONY: build
build:
	go test ./...
	go build -o bin/mixtape github.com/arecker/mixtape/cmd

.PHONY: clean
clean:
	rm -f ./mixtape
