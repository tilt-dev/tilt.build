FROM ruby:2.6

# jekyll has weird behavior where it will force things if in the default (development) environment
# so explicitly set a custom one
# see https://github.com/jekyll/jekyll/issues/5743#issuecomment-271396025
ENV JEKYLL_ENV=docker

RUN gem install jekyll bundler

WORKDIR /src

ADD ./src/Gemfile /src/
ADD ./src/Gemfile.lock /src/
RUN bundle install
