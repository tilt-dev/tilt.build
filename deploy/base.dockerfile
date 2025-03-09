FROM ruby:3.2

# jekyll has weird behavior where it will force things if in the default (development) environment
# so explicitly set a custom one
# see https://github.com/jekyll/jekyll/issues/5743#issuecomment-271396025
ENV JEKYLL_ENV=docker

RUN gem install bundler
RUN gem update --system
RUN gem install jekyll

WORKDIR /src

ADD ./src/Gemfile /src/
ADD ./src/Gemfile.lock /src/
RUN bundle install

ENTRYPOINT ["jekyll"]
