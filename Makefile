.PHONY: api

api:
	docker rm tilt.api || exit 0
	rm -fR api/api.html
	docker build -t tilt.api -f deploy/api.dockerfile .
	docker run --name tilt.api tilt.api
	docker cp tilt.api:/src/functions.html src/_includes/functions.html
	docker cp tilt.api:/src/classes.html src/_includes/classes.html
	docker cp tilt.api:/src/functions.yaml src/_data/api_functions.yaml
	docker cp tilt.api:/src/classes.yaml src/_data/api_classes.yaml
	docker rm tilt.api
