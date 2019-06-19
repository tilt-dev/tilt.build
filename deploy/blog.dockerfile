FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /blog

RUN mkdir -p /src
RUN mkdir -p /blog
ADD src/Gemfile /src/
ADD src/Gemfile.lock /src/
# work around https://github.com/windmilleng/tilt.build/issues/101
ADD blog/Gemfile /blog/
ADD blog/Gemfile.lock /blog/

RUN bundle install
ADD src /src/
ADD blog /blog/
ADD healthcheck.sh .
ENTRYPOINT bundle exec jekyll serve --config _config.yml,_config-dev.yml
