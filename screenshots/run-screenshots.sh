#!/usr/bin/env bash

set -e
docker build -t screenshots:latest screenshots
docker_host=$(docker context inspect | jq -r '.[0].Endpoints.docker.Host')
args=( )
if [ "${docker_host#unix://}" != "${docker_host}" ]; then
    args=( -v "${docker_host#unix://}:/var/run/docker.sock" )
fi
if [ "${docker_host#tcp://localhost:}" != "${docker_host}" ]; then
    args=( -e "DOCKER_HOST=tcp://host.docker.internal:${docker_host#tcp://localhost:}" )
fi
docker rm -f screenshots
docker run "${args[@]}" -v $PWD/docs/assets/docimg:/app/screenshots --name screenshots screenshots:latest
