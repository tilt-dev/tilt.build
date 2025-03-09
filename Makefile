.PHONY: api stars cli-toc build-blog build-docs build-site

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

cli-toc:
	./hack/inject_cli_toc.sh

build-blog:
	rm -fR build/blog
	docker build -t tilt-site-base -f deploy/base.dockerfile .
	docker buildx build --target static --output type=local,dest=build/blog -f deploy/blog.dockerfile .

build-docs:
	rm -fR build/docs
	docker build -t tilt-site-base -f deploy/base.dockerfile .
	docker buildx build --target static --output type=local,dest=build/docs -f deploy/docs.dockerfile .

build-site:
	rm -fR build/site
	docker build -t tilt-site-base -f deploy/base.dockerfile .
	docker buildx build --target static --output type=local,dest=build/site -f deploy/site.dockerfile .
