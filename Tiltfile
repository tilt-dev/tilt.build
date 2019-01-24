# -*- mode: Python -*-

k8s_yaml('serve.yaml')
repo = local_git_repo('.')
img = fast_build('gcr.io/windmill-public-containers/tilt-site',
                 'base.dockerfile',
                 'bundle exec jekyll serve')
img.add(repo.path('src'), '/src/')
img.run('bundle update', trigger=['src/Gemfile', 'src/Gemfile.lock'])
img.hot_reload()

k8s_resource('tilt-site', port_forwards=4000)
