#!/bin/sh

cd $(dirname $0)

set -ex
yarn install
STARS=$(node stars.js)
sed -i'' -e "s/stars: .*/stars: $STARS/" ../src/_data/github.yml
