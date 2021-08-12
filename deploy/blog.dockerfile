FROM tilt-site-base

WORKDIR /blog

RUN mkdir -p /blog
ADD src /src/
ADD blog /blog/
ADD healthcheck.sh .
ENTRYPOINT bundle exec jekyll serve --trace --future --config _config.yml,_config-dev.yml
