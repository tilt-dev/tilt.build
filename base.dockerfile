FROM ruby:2.6

RUN echo hi

RUN echo foo

RUN gem install jekyll bundler

WORKDIR /src
