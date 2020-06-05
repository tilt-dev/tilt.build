#!/bin/sh

cd $(dirname $0)

set -ex
yarn install
STARS=$(node stars.js)
sed -i'' -e "s/githubStars: .*/githubStars: $STARS/" ../src/_data/header2.yml
sed -i'' -e "s/githubStars: .*/githubStars: $STARS/" ../src/_data/footer2.yml
