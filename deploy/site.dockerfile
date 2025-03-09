FROM tilt-site-base AS sources

WORKDIR /src

RUN mkdir -p /src
ADD src /src/
ADD healthcheck.sh .

FROM sources AS static-builder
RUN JEKYLL_ENV=production bundle exec jekyll build -d _site

FROM scratch AS static
COPY --from=static-builder /src/_site /

FROM sources
ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--trace", "--config", "_config.yml,_config-dev.yml"]
