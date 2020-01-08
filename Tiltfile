# -*- mode: Python -*-
set_team('tilt-dev')
enable_feature('update_history')

# Generate the API docs.
local_resource('make-api', 'make api', ['deploy/api.dockerfile', 'Makefile', 'api'])

local_resource(
  'tilt-site',
  cmd='true', # TODO(dmiller): do we need this?
  serve_cmd='cd src && bundle exec jekyll serve --config _config.yml,_config-dev.ym',
  deps='.',
  ignore=['./api', './docs', './blog'],
)

local_resource(
  'docs-site',
  cmd='true', # TODO(dmiller): do we need this?
  serve_cmd='cd docs && bundle exec jekyll serve --config _config.yml,_config-dev.ym',
  deps='.',
  ignore=['./api', './blog'],
  resource_deps=['make-api']
 )

local_resource(
  'blog-site',
  cmd='true', # TODO(dmiller): do we need this?
  serve_cmd='cd blog && bundle exec jekyll serve --config _config.yml,_config-dev.ym',
  deps='.',
  ignore=['./api', './docs'],
)
