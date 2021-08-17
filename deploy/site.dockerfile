FROM tilt-site-base
ADD ./src .
ADD healthcheck.sh .
ENTRYPOINT bundle exec jekyll serve --trace --config _config.yml,_config-dev.yml
