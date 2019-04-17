.PHONY: build api

build:
	docker rm tilt.build || exit 0
	docker build -t tilt.build -f Dockerfile .
	docker run --name tilt.build tilt.build
	docker cp tilt.build:/src .
	docker rm tilt.build

api:
	docker rm tilt.api || exit 0
	rm -fR api/api.html
	docker build -t tilt.api -f api.dockerfile .
	docker run --name tilt.api tilt.api
	docker cp tilt.api:/src/api.html docs/_includes/api.html
	docker rm tilt.api
