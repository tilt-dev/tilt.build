# -*- mode: Python -*-
set_team('tilt-dev')
enable_feature('update_history')

# Generate the API docs.
local_resource('make-api', 'make api', ['deploy/api.dockerfile', 'Makefile', 'api'])

local_resource(
  'tilt-site',
  serve_cmd='cd src && bundle exec jekyll serve -P 4000 --config _config.yml,_config-dev.yml',
  deps=['src/_config.yml', 'src/_config-dev.yml'],
  ignore=['./api', './docs', './blog'],
)

local_resource(
  'docs-site',
  serve_cmd='cd docs && bundle exec jekyll serve -P 4001 --config _config.yml,_config-dev.yml',
  deps=['docs/_config.yml', 'docs/_config-dev.yml'],
  ignore=['./api', './blog'],
  resource_deps=['make-api']
 )

local_resource(
  'blog-site',
  serve_cmd='cd blog && bundle exec jekyll serve -P 4002 --config _config.yml,_config-dev.yml',
  deps=['blog/_config.yml', 'blog/_config-dev.yml'],
  ignore=['./api', './docs'],
)
