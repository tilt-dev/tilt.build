FROM ruby:2.6

RUN gem install jekyll bundler

WORKDIR /src

ADD ./src/Gemfile /src/
ADD ./src/Gemfile.lock /src/
RUN bundle install
