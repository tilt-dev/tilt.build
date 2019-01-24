FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /src

ADD src .

RUN bundle update
