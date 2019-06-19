FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /docs

RUN mkdir -p /src
RUN mkdir -p /docs
ADD src/Gemfile /src/
ADD src/Gemfile.lock /src/
# work around https://github.com/windmilleng/tilt.build/issues/101
ADD docs/Gemfile /docs/
ADD docs/Gemfile.lock /docs/

RUN bundle install
ADD src /src/
ADD docs /docs/
ADD healthcheck.sh .
ENTRYPOINT bundle exec jekyll serve --config _config.yml,_config-dev.yml
