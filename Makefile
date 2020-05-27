.PHONY: api stars

api:
	docker rm tilt.api || exit 0
	rm -fR api/api.html
	DOCKER_BUILDKIT=1 docker build -t tilt.api -f deploy/api.dockerfile .
	docker run --name tilt.api tilt.api
	docker cp tilt.api:/src/functions.yaml src/_data/api/functions.yaml
	docker cp tilt.api:/src/functions.html src/_includes/api/functions.html
	docker cp tilt.api:/src/classes.yaml src/_data/api/classes.yaml
	docker cp tilt.api:/src/classes.html src/_includes/api/classes.html
	docker cp tilt.api:/src/data.yaml src/_data/api/data.yaml
	docker cp tilt.api:/src/data.html src/_includes/api/data.html
	docker rm tilt.api

stars:
	./stars/inject_stars.sh
