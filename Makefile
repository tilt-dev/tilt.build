.PHONY: api

api:
	docker rm tilt.api || exit 0
	rm -fR api/api.html
	docker build -t tilt.api -f deploy/api.dockerfile .
	docker run --name tilt.api tilt.api
	docker cp tilt.api:/src/api.html src/_includes/api.html
	docker rm tilt.api
