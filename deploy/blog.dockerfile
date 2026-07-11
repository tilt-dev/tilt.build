FROM tilt-site-base AS sources

WORKDIR /blog

RUN mkdir -p /blog
ADD src /src/
ADD blog /blog/
ADD healthcheck.sh .

FROM sources AS static-builder
RUN JEKYLL_ENV=production bundle exec jekyll build -d _site
# Also emit each page as <name>/index.html so extensionless URLs work: CloudFront
# rewrites /foo to /foo/index.html, and keeping the .html extension means the S3
# sync tags it text/html automatically.
RUN find _site -type f -name '*.html' ! -name 'index.html' -exec sh -c 'd="${1%.html}"; mkdir -p "$d"; cp "$1" "$d/index.html"' _ {} \;

FROM scratch AS static
COPY --from=static-builder /blog/_site /

FROM sources
ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--trace", "--future", "--config", "_config.yml,_config-dev.yml"]
