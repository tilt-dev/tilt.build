FROM tilt-site-base AS sources

WORKDIR /docs

RUN mkdir -p /docs
ADD src /src/
ADD docs /docs/
ADD healthcheck.sh .

FROM sources AS static-builder
RUN JEKYLL_ENV=production bundle exec jekyll build -d _site

FROM node:22-alpine as search-builder
RUN npm install -g pagefind
WORKDIR /build
COPY --from=static-builder /docs/_site /build
RUN pagefind --site .
# Also emit each page as <name>/index.html so extensionless URLs work: CloudFront
# rewrites /foo to /foo/index.html, and keeping the .html extension means the S3
# sync tags it text/html automatically. Done after pagefind so the copies aren't
# indexed as duplicate search results.
RUN find . -type f -name '*.html' ! -name 'index.html' -exec sh -c 'd="${1%.html}"; mkdir -p "$d"; cp "$1" "$d/index.html"' _ {} \;

FROM scratch AS static
COPY --from=search-builder /build /

FROM sources
ENTRYPOINT ["bundle", "exec", "jekyll", "serve", "--trace", "--config", "_config.yml,_config-dev.yml"]
