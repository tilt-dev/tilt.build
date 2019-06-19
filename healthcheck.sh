#!/bin/sh

set -ex

# check to make sure Jekyll is serving
curl localhost:4000

# check to make sure Jekyll doesn't have any errors
bundle exec jekyll build --config _config.yml,_config-dev.yml
