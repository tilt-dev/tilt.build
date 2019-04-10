FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /src

ADD ./Gemfile* /src/
RUN bundle install
ADD . .
ENTRYPOINT bundle exec jekyll serve --config _config.yml,_config-dev.yml
