FROM tilt-site-base AS sources

WORKDIR /blog

RUN mkdir -p /blog
ADD src /src/
ADD blog /blog/
ADD healthcheck.sh .

FROM sources AS static-builder
RUN JEKYLL_ENV=production bundle exec jekyll build -d _site
# Create extensionless copies of every page (foo.html -> foo) so URLs work both
# with and without the ".html" suffix once synced to S3.
RUN find _site -type f -name '*.html' ! -name 'index.html' -exec sh -c 'cp "$1" "${1%.html}"' _ {} \;

FROM scratch AS static
COPY --from=static-builder /blog/_site /

FROM sources
ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--trace", "--future", "--config", "_config.yml,_config-dev.yml"]
