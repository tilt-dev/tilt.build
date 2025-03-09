FROM tilt-site-base AS sources

WORKDIR /blog

RUN mkdir -p /blog
ADD src /src/
ADD blog /blog/
ADD healthcheck.sh .

FROM sources AS static-builder
RUN JEKYLL_ENV=production bundle exec jekyll build -d _site

FROM scratch AS static
COPY --from=static-builder /blog/_site /

FROM sources
ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--trace", "--future", "--config", "_config.yml,_config-dev.yml"]
