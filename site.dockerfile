FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /src

ADD ./src/Gemfile /src/
ADD ./src/Gemfile.lock /src/
RUN bundle install
ADD ./src .
ENTRYPOINT bundle exec jekyll serve --config _config.yml,_config-dev.yml
