.PHONY: build

build:
	docker rm tilt.build || exit 0
	docker build -t tilt.build -f Dockerfile .
	docker run --name tilt.build tilt.build
	docker cp tilt.build:/src .
	docker rm tilt.build
