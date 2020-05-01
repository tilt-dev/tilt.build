FROM tilt-site-base

WORKDIR /docs

RUN mkdir -p /docs
ADD src /src/
ADD docs /docs/
ADD healthcheck.sh .
ENTRYPOINT bundle exec jekyll serve --config _config.yml,_config-dev.yml
