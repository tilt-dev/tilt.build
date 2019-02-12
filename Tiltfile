# -*- mode: Python -*-

# Generate the API docs.
read_file('api/api.py')
local('make api')

k8s_yaml('serve.yaml')
repo = local_git_repo('.')

img = fast_build('gcr.io/windmill-public-containers/tilt-site',
                 'base.dockerfile',
                 'echo hi3 && bundle exec jekyll serve --config _config.yml,_config-dev.yml')
img.add(repo.path('src'), '/src/')
img.run('bundle update', trigger=['src/Gemfile', 'src/Gemfile.lock'])
img.hot_reload()

img = fast_build('gcr.io/windmill-public-containers/docs-site',
                 'docs.dockerfile',
                 'bundle exec jekyll serve --config _config.yml,_config-dev.yml')
img.add(repo.path('src'), '/src/')
img.add(repo.path('docs'), '/docs/')
img.run('bundle update', trigger=['src/Gemfile', 'src/Gemfile.lock', 'docs/Gemfile', 'docs/Gemfile.lock'])
img.hot_reload()

k8s_resource('tilt-site', port_forwards=4000)
k8s_resource('docs-site', port_forwards=4001)
