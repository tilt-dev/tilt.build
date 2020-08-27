#!/bin/sh

cd $(dirname $0)

set -ex
yarn install
STARS=$(node stars.js)
sed -i.bak -e "s/stars: .*/stars: $STARS/" ../src/_data/github.yml
rm -f ../src/_data/github.yml.bak
