#!/bin/bash

while true
do
	echo "running for 5s"
  timeout 5s bundle exec jekyll serve --config _config.yml,_config-dev.yml

  echo "sleeping 10s"
	sleep 10
done
